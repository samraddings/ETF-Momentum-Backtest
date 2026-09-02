import numpy as np
import pandas as pd

def annualised_return(returns):
    """Annualised return from a series of daily returns."""
    total_return = (1 + returns).prod() - 1
    n_days = len(returns)
    return (1 + total_return) ** (252 / n_days) - 1

def annualised_volatility(returns):
    """Annualised volatility from daily returns."""
    return returns.std() * np.sqrt(252)

def sharpe_ratio(returns, risk_free_rate=0):
    """Annualised Sharpe ratio assuming daily returns and zero risk-free rate by default."""
    excess_returns = returns - risk_free_rate / 252
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

def max_drawdown(returns):
    """Maximum drawdown from a series of daily returns (negative number)."""
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    drawdown = cum / running_max - 1
    return drawdown.min()