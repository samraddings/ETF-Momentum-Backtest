import pandas as pd

def monthly_weights_to_daily(monthly_weights, daily_index):
    """
    Convert monthly rebalanced weights to daily positions.

    The weights at month-end t apply to trading days of month t+1.
    We achieve this by shifting the monthly weights by one period, then
    forward-filling on the daily index.

    Parameters:
    - monthly_weights: DataFrame with monthly index and ticker columns.
    - daily_index: DatetimeIndex of daily trading days.

    Returns:
    - daily_weights: DataFrame with same index as daily_index, columns = tickers.
    """
    # Shift: month-end weight for month t becomes effective at start of month t+1
    shifted = monthly_weights.shift(1)
    # Reindex to daily dates, forward fill
    daily_weights = shifted.reindex(daily_index, method='ffill')
    # Fill initial NaN with 0 (no positions before first rebalance)
    daily_weights = daily_weights.fillna(0.0)
    return daily_weights