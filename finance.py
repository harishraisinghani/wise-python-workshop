from pandas import Series, DataFrame
from pandas_datareader import data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

os.environ["IEX_API_KEY"] = "pk_acd84b8074134c629bf5db6990c67a38"


tickers = ['AAPL', 'AMZN', 'MSFT']

start_date = '2019-01-01'
end_date = '2019-10-01'

stock_data = data.DataReader(tickers, 'iex', start_date, end_date)

close_data = stock_data['close']

# Plot closing price on single chart
fig, ax = plt.subplots(figsize=(16,9))
ax.plot(close_data.index, close_data['AAPL'], label='AAPL')
ax.plot(close_data.index, close_data['AMZN'], label='AMZN')
ax.plot(close_data.index, close_data['MSFT'], label='MSFT')

ax.set_xlabel('Date')
ax.set_ylabel('Closing price ($)')
ax.legend()

plt.show()


# Plot Weighted Averages on single chart
amzn = close_data.loc[:, 'AMZN']

short_rolling_amzn = amzn.rolling(window=20).mean()
long_rolling_amzn = amzn.rolling(window=100).mean()

ax.plot(amzn.index, amzn, label='AMZN')
ax.plot(short_rolling_amzn.index, short_rolling_amzn, label='20 days rolling')
ax.plot(long_rolling_amzn.index, long_rolling_amzn, label='100 days rolling')

ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.set_title('Moving average of some tech stocks')
ax.legend()

plt.show()

# Plot Log and Relative Returns on separate plots

relative_returns = close_data.pct_change(1)
relative_returns.head()

log_returns = np.log(close_data).diff()
log_returns.head()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))

for c in log_returns:
    ax1.plot(log_returns.index, log_returns[c].cumsum(), label=str(c))

ax1.set_ylabel('Cumulative log returns')
ax1.legend(loc='best')

for c in relative_returns:
    ax2.plot(relative_returns.index, 100*(np.exp(log_returns[c].cumsum()) - 1), label=str(c))

ax2.set_ylabel('Total relative returns (%)')
ax2.legend(loc='best')

plt.show()

# Basic Trading Strategy

r_t = log_returns.tail(1).transpose()
weights_vector = pd.DataFrame(1 / 3, index=r_t.index, columns=r_t.columns)
portfolio_log_return = weights_vector.transpose().dot(r_t)

# Moving Average Trading Strategy

ema_short = close_data.ewm(span=20, adjust=False).mean()
trading_positions_raw = close_data - ema_short
trading_positions = trading_positions_raw
trading_positions_raw[trading_positions_raw <= 0] = 0
trading_positions = trading_positions_raw.apply(np.sign)*1/3

asset_log_returns = np.log(close_data).diff()
strategy_asset_log_returns = trading_positions_final * asset_log_returns

