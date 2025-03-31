def moving_average_strategy(df):
    df["signal"] = 0
    df["sma50"] = df["close"].rolling(window=50).mean()
    df["sma200"] = df["close"].rolling(window=200).mean()

    df.loc[df["sma50"] > df["sma200"], "signal"] = 1   # Buy
    df.loc[df["sma50"] < df["sma200"], "signal"] = -1  # Sell

    return df
