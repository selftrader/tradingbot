import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import yaml

# Configuration (normally in config.yaml)
CONFIG = {
    "data": {"csv_path": "C:\Work\P\app\tradingapp-main\tradingapp-main\data\processed\NIFTY IT\TCS.NS_historical.csv"},
    "strategy": {"type": "fibonacci", "lookback": 20, "stop_loss_pct": 0.02, "target_pct": 0.05},
    "capital": {"initial": 100000},
    "trading": {"shares_per_trade": 100, "broker_fee": 20}
}

# Setup logging
logging.basicConfig(filename="backtest_report.log", level=logging.INFO)

# Data Loader
def load_csv_data(csv_path):
    data = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
    return data['Close']  # Adjust if column name differs

# Fibonacci Strategy
def fibonacci_strategy(prices, lookback=20, stop_loss_pct=0.02, target_pct=0.05):
    signals = pd.DataFrame(index=prices.index)
    signals['price'] = prices
    signals['high'] = prices.rolling(window=lookback).max()
    signals['low'] = prices.rolling(window=lookback).min()
    signals['fib_382'] = signals['low'] + (signals['high'] - signals['low']) * 0.382
    signals['fib_50'] = signals['low'] + (signals['high'] - signals['low']) * 0.5
    signals['fib_618'] = signals['low'] + (signals['high'] - signals['low']) * 0.618
    
    signals['signal'] = 0
    signals['stop_loss'] = np.nan
    signals['target'] = np.nan
    
    for i in range(lookback, len(signals)):
        if signals['price'].iloc[i] > signals['fib_50'].iloc[i-1] and signals['signal'].iloc[i-1] == 0:
            signals['signal'].iloc[i] = 1
            signals['stop_loss'].iloc[i] = signals['price'].iloc[i] * (1 - stop_loss_pct)
            signals['target'].iloc[i] = signals['price'].iloc[i] * (1 + target_pct)
        elif signals['signal'].iloc[i-1] == 1:
            if signals['price'].iloc[i] <= signals['stop_loss'].iloc[i-1]:
                signals['signal'].iloc[i] = -1
            elif signals['price'].iloc[i] >= signals['target'].iloc[i-1]:
                signals['signal'].iloc[i] = -1
            else:
                signals['signal'].iloc[i] = 1
    
    signals['positions'] = signals['signal'].diff()
    return signals

# Advanced Metrics Calculation
def calculate_metrics(portfolio, trades):
    returns = portfolio['returns'].dropna()
    total_trades = len(trades)
    wins = sum(1 for t in trades if t['profit'] > 0)
    losses = total_trades - wins
    win_ratio = wins / total_trades if total_trades > 0 else 0
    
    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if returns.std() != 0 else 0
    rolling_max = portfolio['total'].cummax()
    drawdown = (portfolio['total'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    gross_profit = sum(t['profit'] for t in trades if t['profit'] > 0)
    gross_loss = abs(sum(t['profit'] for t in trades if t['profit'] < 0))
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else np.inf
    
    return {
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses,
        'win_ratio': win_ratio,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'profit_factor': profit_factor
    }

# Backtesting Engine
def backtest(signals, initial_capital=100000, shares_per_trade=100, broker_fee=20):
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions['stock'] = shares_per_trade * signals['signal'].shift(1).fillna(0)
    
    portfolio = pd.DataFrame(index=signals.index)
    portfolio['price'] = signals['price']
    portfolio['holdings'] = positions['stock'] * signals['price']
    pos_diff = positions.diff()
    
    portfolio['cash'] = initial_capital - (pos_diff['stock'] * signals['price']).cumsum()
    portfolio['cash'] -= pos_diff['stock'].abs() * broker_fee / shares_per_trade
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    
    trades = []
    balance_used = initial_capital
    entry_price = 0
    
    for i in range(1, len(signals)):
        if signals['positions'].iloc[i] == 1:
            entry_price = signals['price'].iloc[i]
            stop_loss = signals['stop_loss'].iloc[i]
            target = signals['target'].iloc[i]
            balance_used = max(balance_used, entry_price * shares_per_trade + broker_fee)
        elif signals['positions'].iloc[i] == -1 and signals['signal'].iloc[i-1] == 1:
            exit_price = signals['price'].iloc[i]
            profit = (exit_price - entry_price) * shares_per_trade - 2 * broker_fee
            outcome = ("Target Hit" if exit_price >= target else 
                       "Stop-Loss Hit" if exit_price <= stop_loss else "Manual Exit")
            trades.append({
                'entry_date': signals.index[i-1],
                'exit_date': signals.index[i],
                'entry_price': entry_price,
                'exit_price': exit_price,
                'stop_loss': stop_loss,
                'target': target,
                'profit': profit,
                'outcome': outcome
            })
    
    metrics = calculate_metrics(portfolio, trades)
    report = {
        'final_balance': portfolio['total'].iloc[-1],
        'total_return': (portfolio['total'].iloc[-1] - initial_capital) / initial_capital * 100,
        'max_balance_used': balance_used,
        'timeframe': f"{signals.index[0]} to {signals.index[-1]}",
        'trades': trades,
        **metrics
    }
    
    logging.info(f"Backtest Report:")
    logging.info(f"Timeframe: {report['timeframe']}")
    logging.info(f"Total Trades: {report['total_trades']}")
    logging.info(f"Wins: {report['wins']}, Losses: {report['losses']}")
    logging.info(f"Win Ratio: {report['win_ratio']:.2%}")
    logging.info(f"Sharpe Ratio: {report['sharpe_ratio']:.2f}")
    logging.info(f"Max Drawdown: {report['max_drawdown']:.2%}")
    logging.info(f"Profit Factor: {report['profit_factor']:.2f}")
    logging.info(f"Final Balance: ₹{report['final_balance']:.2f}")
    logging.info(f"Total Return: {report['total_return']:.2f}%")
    logging.info(f"Max Balance Used: ₹{report['max_balance_used']:.2f}")
    logging.info("Trade Details:")
    for trade in trades:
        logging.info(f"{trade['entry_date']} - {trade['exit_date']}: Buy@₹{trade['entry_price']:.2f}, "
                     f"Sell@₹{trade['exit_price']:.2f}, SL:₹{trade['stop_loss']:.2f}, "
                     f"Tgt:₹{trade['target']:.2f}, Profit:₹{trade['profit']:.2f}, {trade['outcome']}")
    
    return portfolio, report

# Advanced Plotting
def plot_advanced_results(signals, portfolio, report):
    fig = plt.figure(figsize=(15, 10))
    
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(signals['price'], label='Price', color='blue')
    ax1.plot(signals['fib_50'], label='Fib 50%', color='orange', linestyle='--')
    ax1.plot(signals['fib_382'], label='Fib 38.2%', color='green', linestyle='--')
    ax1.plot(signals['fib_618'], label='Fib 61.8%', color='purple', linestyle='--')
    
    buy_signals = signals[signals['positions'] == 1]
    sell_signals = signals[signals['positions'] == -1]
    ax1.plot(buy_signals.index, buy_signals['price'], '^', markersize=10, color='g', label='Buy')
    ax1.plot(sell_signals.index, sell_signals['price'], 'v', markersize=10, color='r', label='Sell')
    
    for i in range(len(buy_signals)):
        ax1.axhline(y=buy_signals['stop_loss'].iloc[i], xmin=0, xmax=1, color='r', linestyle=':', alpha=0.5)
        ax1.axhline(y=buy_signals['target'].iloc[i], xmin=0, xmax=1, color='g', linestyle=':', alpha=0.5)
    
    ax1.legend()
    ax1.set_title(f"Price with Fibonacci Levels and Signals (Win Ratio: {report['win_ratio']:.2%})")
    
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(portfolio['total'], label='Portfolio Value (₹)', color='blue')
    ax2.legend()
    ax2.set_title('Portfolio Value Over Time')
    
    ax3 = fig.add_subplot(3, 1, 3)
    rolling_max = portfolio['total'].cummax()
    drawdown = (portfolio['total'] - rolling_max) / rolling_max
    ax3.plot(drawdown, label='Drawdown', color='red')
    ax3.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    ax3.legend()
    ax3.set_title(f"Drawdown (Max: {report['max_drawdown']:.2%})")
    
    plt.tight_layout()
    plt.show()

# Main Execution
if __name__ == "__main__":
    config = CONFIG
    prices = load_csv_data(config['data']['csv_path'])
    signals = fibonacci_strategy(prices, config['strategy']['lookback'], 
                                config['strategy']['stop_loss_pct'], config['strategy']['target_pct'])
    portfolio, report = backtest(signals, config['capital']['initial'], 
                                config['trading']['shares_per_trade'], config['trading']['broker_fee'])
    
    print("Backtest Summary:")
    print(f"Timeframe: {report['timeframe']}")
    print(f"Total Trades: {report['total_trades']}")
    print(f"Wins: {report['wins']}, Losses: {report['losses']}")
    print(f"Win Ratio: {report['win_ratio']:.2%}")
    print(f"Sharpe Ratio: {report['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {report['max_drawdown']:.2%}")
    print(f"Profit Factor: {report['profit_factor']:.2f}")
    print(f"Final Balance: ₹{report['final_balance']:.2f}")
    print(f"Total Return: {report['total_return']:.2f}%")
    print(f"Max Balance Used: ₹{report['max_balance_used']:.2f}")
    print("Check backtest_report.log for detailed trade report.")
    
    plot_advanced_results(signals, portfolio, report)