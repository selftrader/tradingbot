import pandas as pd
import matplotlib.pyplot as plt

# === CONFIG ===
CSV_PATH = r'C:\Work\P\app\tradingapp-main\tradingapp-main\data\processed\NIFTY IT\TCS.NS_historical.csv'  # Update with your file path
INITIAL_CAPITAL = 1000000
STOP_LOSS_PCT = 0.15     # 15% SL
TARGET_PCT = 0.25        # 25% Target
HOLD_CANDLES = 6         # Hold trade for up to 6 candles
LOT_SIZE = 50            # Lot size for option
POSITION_SIZE = 1        # Number of lots per trade
FIB_LOOKBACK = 50        # No. of candles to calculate Fib

# === LOAD DATA ===
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip()
datetime_col = [col for col in df.columns if 'time' in col.lower()][0]
df[datetime_col] = pd.to_datetime(df[datetime_col])
df.rename(columns={datetime_col: 'Timestamp'}, inplace=True)
df = df.sort_values('Timestamp').reset_index(drop=True)

# Calculate EMAs for trend filtering
df['EMA21'] = df['UnderlyingPrice'].rolling(window=21).mean()
df['EMA55'] = df['UnderlyingPrice'].rolling(window=55).mean()

# Fibonacci calculator
def get_fibonacci_levels(high, low):
    diff = high - low
    return {
        '0.618': high - 0.618 * diff,
        '0.5': high - 0.5 * diff,
        '0.382': high - 0.382 * diff
    }

# === BACKTEST ===
capital = INITIAL_CAPITAL
wins, losses = 0, 0
trades = []

for i in range(FIB_LOOKBACK, len(df) - HOLD_CANDLES):
    recent_high = df['UnderlyingPrice'].iloc[i - FIB_LOOKBACK:i].max()
    recent_low = df['UnderlyingPrice'].iloc[i - FIB_LOOKBACK:i].min()
    fib = get_fibonacci_levels(recent_high, recent_low)
    entry_zone = fib['0.618']

    current = df.iloc[i]
    next_candles = df.iloc[i+1:i+HOLD_CANDLES+1]

    # Entry condition
    if (
        current['UnderlyingPrice'] <= entry_zone + 5 and
        current['UnderlyingPrice'] >= entry_zone - 5 and
        current['UnderlyingPrice'] > current['EMA21'] > current['EMA55']
    ):
        entry_premium = current['Close']  # option premium
        sl = entry_premium * (1 - STOP_LOSS_PCT)
        target = entry_premium * (1 + TARGET_PCT)
        outcome = 'No Hit'
        hit = False

        for j in range(len(next_candles)):
            row = next_candles.iloc[j]
            if row['Low'] <= sl:
                loss = (entry_premium - sl) * LOT_SIZE * POSITION_SIZE
                capital -= loss
                losses += 1
                outcome = f'SL Hit (Candle {j+1})'
                hit = True
                break
            elif row['High'] >= target:
                profit = (target - entry_premium) * LOT_SIZE * POSITION_SIZE
                capital += profit
                wins += 1
                outcome = f'Target Hit (Candle {j+1})'
                hit = True
                break

        if not hit:
            exit_price = next_candles.iloc[-1]['Close']
            pnl = (exit_price - entry_premium) * LOT_SIZE * POSITION_SIZE
            capital += pnl
            if pnl > 0:
                wins += 1
                outcome = 'Exit Green (No Hit)'
            else:
                losses += 1
                outcome = 'Exit Red (No Hit)'

        trades.append({
            'Timestamp': current['Timestamp'],
            'Underlying': round(current['UnderlyingPrice'], 2),
            'Buy Premium': round(entry_premium, 2),
            'Target': round(target, 2),
            'Stop Loss': round(sl, 2),
            'Outcome': outcome,
            'Capital After Trade': round(capital, 2)
        })

# === RESULTS ===
total_trades = wins + losses
win_rate = (wins / total_trades) * 100 if total_trades else 0
net_pnl = capital - INITIAL_CAPITAL

print("\n📊 Backtest Summary")
print(f"Total Trades   : {total_trades}")
print(f"Wins           : {wins}")
print(f"Losses         : {losses}")
print(f"Win Rate       : {win_rate:.2f}%")
print(f"Final Capital  : ₹{capital:.2f}")
print(f"Net P&L        : ₹{net_pnl:.2f}")

# Save report
report_df = pd.DataFrame(trades)
report_df.to_csv('option_fibonacci_backtest_report.csv', index=False)
print("\n✅ Report saved: option_fibonacci_backtest_report.csv")

# Outcome chart
report_df['Outcome'].value_counts().plot(kind='bar', title='Trade Outcomes', figsize=(8,4))
plt.ylabel('Count')
plt.xlabel('Outcome')
plt.grid(True)
plt.tight_layout()
plt.show()
