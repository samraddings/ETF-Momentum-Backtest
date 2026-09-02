import pandas as pd

def moving_average_crossover(prices, short_window=50, long_window=200):
    """
    Generate trading signals for a single asset using moving average crossover.

    Parameters:
    - prices: pandas Series of daily prices (adjusted close).
    - short_window: short moving average window (default 50).
    - long_window: long moving average window (default 200).

    Returns:
    - position: pandas Series of positions (1 = long, 0 = flat) aligned with prices index.
                Position is shifted by one day to avoid look-ahead bias.
    """
    short_ma = prices.rolling(window=short_window).mean()
    long_ma = prices.rolling(window=long_window).mean()
    # Signal: 1 if short MA > long MA, else 0
    signal = (short_ma > long_ma).astype(int)
    # Shift by one day: trade only based on information available at previous close
    position = signal.shift(1)
    return position