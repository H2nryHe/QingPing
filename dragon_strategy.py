import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA10'] = data['Close'].rolling(window=10).mean()
    data['Volume_MA5'] = data['Volume'].rolling(window=5).mean()
    return data


def dragon_strategy(data):
    buy_signals = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    # print('len(buy_signals)', len(buy_signals))
    sell_signals = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    position = False
    buy_prices = []
    sell_prices = []
    returns = []

    for i in range(10, len(data)):
        # buy signal
        if (data['Close'][i] > data['MA5'][i] and data['Close'][i - 1] < data['MA5'][i - 1]) and \
                (data['Volume'][i] < data['Volume_MA5'][i] and data['Volume'][i - 1] < data['Volume_MA5'][i - 1]):
            buy_signals.append(data['Close'][i])
            sell_signals.append(np.nan)
            buy_prices.append(data['Close'][i])
            position = True
        # sell signal
        elif position and (data['Close'][i] < data['MA10'][i]):
            sell_signals.append(data['Close'][i])
            buy_signals.append(np.nan)
            sell_prices.append(data['Close'][i])
            position = False
            return_rate = (sell_prices[-1] - buy_prices[-1]) / buy_prices[-1]
            returns.append(return_rate)
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)
    # print('length of buy_signals: ', len(buy_signals))
    # print('length of sell_signals: ', len(sell_signals))
    # print('length of buy_signals_data: ', len(data))
    data['Buy_Signal'] = buy_signals
    data['Sell_Signal'] = sell_signals

    total_return = np.sum(returns)
    return data, total_return, returns


def plot_signals(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['MA5'], label='5 Day MA', alpha=0.5)
    plt.plot(data['MA10'], label='10 Day MA', alpha=0.5)
    plt.scatter(data.index, data['Buy_Signal'], label='Buy Signal', marker='^', color='green', alpha=1)
    plt.scatter(data.index, data['Sell_Signal'], label='Sell Signal', marker='v', color='red', alpha=1)
    plt.title('Stock Price with Dragon Strategy Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2024-01-01"

data = get_stock_data(ticker, start=start_date, end=end_date)
data, total_return, returns = dragon_strategy(data)
plot_signals(data)

print(f"龙回头战法的总回报率: {total_return * 100:.2f}%")