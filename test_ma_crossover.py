import pandas as pd
import matplotlib.pyplot as plt
from data import download_data, clean_data
from strategies import moving_average_crossover
from metrics import annualised_return, annualised_volatility, sharpe_ratio, max_drawdown

# 1. Load data
tickers = ['SPY', 'QQQ', 'IWM', 'TLT', 'GLD', 'EFA']
data = clean_data(download_data(tickers))
spy_prices = data['SPY']

# 2. Generate positions
position = moving_average_crossover(spy_prices, short_window=50, long_window=200)

# 3. Compute daily returns
daily_returns = spy_prices.pct_change().dropna()
strategy_returns = daily_returns * position

# 4. Buy-and-hold returns (same as daily_returns when in market every day)
buy_hold_returns = daily_returns

# 5. Print metrics
print("Strategy Annualised Return:", annualised_return(strategy_returns))
print("Buy & Hold Annualised Return:", annualised_return(buy_hold_returns))
print("Strategy Annualised Volatility:", annualised_volatility(strategy_returns))
print("Strategy Sharpe Ratio:", sharpe_ratio(strategy_returns))
print("Strategy Max Drawdown:", max_drawdown(strategy_returns))

# 6. Plot equity curves
cum_strategy = (1 + strategy_returns).cumprod()
cum_bh = (1 + buy_hold_returns).cumprod()

plt.figure(figsize=(12,6))
plt.plot(cum_strategy, label='MA Crossover (50/200)')
plt.plot(cum_bh, label='Buy & Hold SPY')
plt.title('SPY Moving Average Crossover vs Buy & Hold')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.savefig('plots/ma_crossover_equity.png')  # ensure plots folder exists
plt.show()