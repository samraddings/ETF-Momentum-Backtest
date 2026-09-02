import pandas as pd
import matplotlib.pyplot as plt
from data import download_data, clean_data
from strategies import monthly_momentum_signal, top_n_momentum_weights
from backtest import monthly_weights_to_daily
from metrics import annualised_return, annualised_volatility, sharpe_ratio, max_drawdown

# 1. Load and clean data
tickers = ['SPY', 'QQQ', 'IWM', 'TLT', 'GLD', 'EFA']
data = clean_data(download_data(tickers))
daily_returns = data.pct_change().dropna()

# 2. Cross-sectional momentum
lookback = 60
monthly_mom = monthly_momentum_signal(data, lookback)
monthly_weights = top_n_momentum_weights(monthly_mom, n=3)
daily_weights = monthly_weights_to_daily(monthly_weights, daily_returns.index)
momentum_returns = (daily_weights * daily_returns).sum(axis=1)

# 3. Benchmark: equal-weight all assets, rebalanced monthly
# Create monthly equal weights (1/len(tickers) for each ticker)
monthly_equal_weights = pd.DataFrame(1/len(tickers), index=monthly_weights.index, columns=tickers)
benchmark_weights = monthly_weights_to_daily(monthly_equal_weights, daily_returns.index)
benchmark_returns = (benchmark_weights * daily_returns).sum(axis=1)

# 4. Calculate metrics for both
metrics = {
    'Momentum': [
        annualised_return(momentum_returns),
        annualised_volatility(momentum_returns),
        sharpe_ratio(momentum_returns),
        max_drawdown(momentum_returns)
    ],
    'Benchmark': [
        annualised_return(benchmark_returns),
        annualised_volatility(benchmark_returns),
        sharpe_ratio(benchmark_returns),
        max_drawdown(benchmark_returns)
    ]
}
metrics_df = pd.DataFrame(metrics, index=['Ann. Return', 'Ann. Vol', 'Sharpe', 'Max DD'])
print(metrics_df.round(4))

# 5. Plot equity curves
cum_mom = (1 + momentum_returns).cumprod()
cum_bench = (1 + benchmark_returns).cumprod()

plt.figure(figsize=(12,6))
plt.plot(cum_mom, label='Momentum (Top 3)')
plt.plot(cum_bench, label='Equal-Weight Benchmark')
plt.title('Cross-Sectional Momentum vs Benchmark')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.savefig('plots/momentum_equity.png')
plt.show()

# 6. Plot drawdowns
def drawdown_series(returns):
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    return cum / running_max - 1

dd_mom = drawdown_series(momentum_returns)
dd_bench = drawdown_series(benchmark_returns)

plt.figure(figsize=(12,4))
plt.plot(dd_mom, label='Momentum')
plt.plot(dd_bench, label='Benchmark')
plt.title('Drawdown Comparison')
plt.xlabel('Date')
plt.ylabel('Drawdown')
plt.legend()
plt.grid(True)
plt.savefig('plots/momentum_drawdown.png')
plt.show()