import os
import pandas as pd
import matplotlib.pyplot as plt
from data import download_data, clean_data
from strategies import moving_average_crossover, monthly_momentum_signal, top_n_momentum_weights
from backtest import monthly_weights_to_daily
from metrics import annualised_return, annualised_volatility, sharpe_ratio, max_drawdown, rolling_sharpe

def main():
    # Create plots directory if it doesn't exist
    os.makedirs('plots', exist_ok=True)

    # 1. Data
    tickers = ['SPY', 'QQQ', 'IWM', 'TLT', 'GLD', 'EFA']
    data = clean_data(download_data(tickers))
    daily_returns = data.pct_change().dropna()

    # 2. Cross-sectional momentum strategy
    lookback = 60
    monthly_mom = monthly_momentum_signal(data, lookback)
    monthly_weights = top_n_momentum_weights(monthly_mom, n=3)
    daily_weights = monthly_weights_to_daily(monthly_weights, daily_returns.index)
    momentum_returns = (daily_weights * daily_returns).sum(axis=1)

    # 3. Equal-weight benchmark (monthly rebalanced)
    monthly_equal_weights = pd.DataFrame(1/len(tickers), index=monthly_weights.index, columns=tickers)
    benchmark_weights = monthly_weights_to_daily(monthly_equal_weights, daily_returns.index)
    benchmark_returns = (benchmark_weights * daily_returns).sum(axis=1)

    # 4. Compute metrics for momentum vs benchmark
    metrics_df = pd.DataFrame({
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
    }, index=['Ann. Return', 'Ann. Vol', 'Sharpe', 'Max DD'])
    print("Performance Metrics (Momentum vs Equal-Weight Benchmark)")
    print(metrics_df.round(4))

    # 5. Plots
    # Equity curves
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
    plt.savefig('plots/equity_curve.png')
    plt.close()   # close without showing

    # Drawdowns
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
    plt.savefig('plots/drawdown.png')
    plt.close()

    # Rolling Sharpe (1-year)
    roll_sharpe_mom = rolling_sharpe(momentum_returns, window=252)
    roll_sharpe_bench = rolling_sharpe(benchmark_returns, window=252)
    plt.figure(figsize=(12,4))
    plt.plot(roll_sharpe_mom, label='Momentum')
    plt.plot(roll_sharpe_bench, label='Benchmark')
    plt.title('Rolling 1-Year Sharpe Ratio')
    plt.xlabel('Date')
    plt.ylabel('Sharpe')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/rolling_sharpe.png')
    plt.close()

    print("Plots saved to /plots")

if __name__ == '__main__':
    main()