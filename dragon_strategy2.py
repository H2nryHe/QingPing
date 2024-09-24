import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_stock_data(ticker, start_date, end_date):
    stock = yf.download(ticker, start=start_date, end=end_date)
    return stock


def detect_pullback(stock_data, period=20):
    stock_data['20_high'] = stock_data['Close'].rolling(window=period).max()
    stock_data['pullback'] = (stock_data['20_high'] - stock_data['Close']) / stock_data['20_high'] * 100
    return stock_data


def dragon_tail_strategy(stock_data, pullback_threshold=20, volume_increase=1.5):
    signals = []
    for i in range(1, len(stock_data)):
        if (stock_data['pullback'][i] > pullback_threshold and
                stock_data['Volume'][i] > stock_data['Volume'][i - 1] * volume_increase):
            signals.append(i)
    return signals


def plot_signals(stock_data, signals):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label='Close Price')
    plt.scatter(stock_data.iloc[signals].index, stock_data.iloc[signals]['Close'], color='red', marker='^',
                label='Buy Signal')
    plt.title('Dragon Tail Strategy Signals')
    plt.legend()
    plt.show()


ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'

stock_data = get_stock_data(ticker, start_date, end_date)
stock_data = detect_pullback(stock_data)

signals = dragon_tail_strategy(stock_data)

plot_signals(stock_data, signals)
