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

def momentum_signal(prices, lookback=60):
    """
    Compute momentum signal: past return over lookback days.
    Returns a DataFrame with same shape as prices, values are returns.
    """
    return prices.pct_change(periods=lookback)

def monthly_momentum_signal(prices, lookback=60):
    """
    Compute momentum signal at month-end (last trading day of each month).
    Returns a DataFrame with index = month-end dates, columns = tickers.
    """
    daily_mom = momentum_signal(prices, lookback)
    monthly_mom = daily_mom.resample('ME').last()
    return monthly_mom

def top_n_momentum_weights(monthly_mom, n=3):
    """
    Convert monthly momentum signals into equal-weight portfolio holdings.
    For each month, select top n assets by momentum and assign equal weight (1/n).
    Returns a DataFrame with same index as monthly_mom, columns = tickers.
    """
    ranks = monthly_mom.rank(axis=1, ascending=False, method='first')
    selected = (ranks <= n).astype(float)
    weights = selected.div(selected.sum(axis=1), axis=0)
    return weights