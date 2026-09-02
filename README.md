# ETF Momentum Backtest

## Overview
This project backtests a monthly cross-sectional momentum strategy on a universe of 6 liquid ETFs from 2010 to 2025. The strategy ranks ETFs by their past 60-day return and holds the top 3 with equal weight for one month. It also includes a simple moving-average crossover as a warm-up and an equal-weight benchmark for comparison.

## Data
- Source: Yahoo Finance via `yfinance`
- Tickers: SPY, QQQ, IWM, TLT, GLD, EFA
- Adjusted close prices, daily frequency
- Missing values forward-filled and dropped

## Methodology
1. Compute 60-day returns for each asset.
2. At each month-end, rank assets by past return.
3. Select top 3 and allocate equal weight.
4. Rebalance monthly; positions shifted by one day to avoid look-ahead bias.
5. Compare against equal-weight buy-and-hold benchmark (monthly rebalanced).
6. Performance metrics: annualised return, volatility, Sharpe ratio, max drawdown, rolling Sharpe.

## Results
- Momentum portfolio annualised return: 10.87%
- Benchmark annualised return: 11.18%
- Sharpe ratio: 0.81
- Maximum drawdown: -25.60%
- Equity curve, drawdown, and rolling Sharpe shown in `/plots`

## Limitations
- No transaction costs or slippage modelled.
- Survivorship bias in chosen ETFs.
- Short lookback period not optimised.
- Risk-free rate assumed zero.

## How to run
`pip install -r requirements.txt`
`python main.py`
