import yfinance as yf
import pandas as pd

def download_data(tickers, start='2010-01-01', end='2025-12-31'):
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)['Close']
    data = data.dropna(how='all')
    return data

def clean_data(data):
    """Handle missing values: forward fill then drop remaining NaNs."""
    data = data.ffill().dropna()
    return data

if __name__ == '__main__':
    tickers = ['SPY', 'QQQ', 'IWM', 'TLT', 'GLD', 'EFA']
    raw = download_data(tickers)
    clean = clean_data(raw)
    clean.to_csv('etf_prices.csv')
    print(f"Data shape: {clean.shape}")
    print(clean.head())