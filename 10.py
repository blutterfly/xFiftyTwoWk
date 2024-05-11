import pandas as pd
import yfinance as yf

# Fetch historical data for a stock
data = yf.download('NVDA', start='2020-01-01')

# Calculate the 52-week high for each day
data['52_Week_High'] = data['High'].rolling(window=252).max()

# Identify days where the high price was a new 52-week high
data['Is_New_High'] = data['High'] == data['52_Week_High']

# Create a shifted column for high prices that starts after a new 52-week high
# We will shift by -1 because we want the SMA starting the day after the new high
data['Shifted_High'] = data['High'].shift(-1)

# For each day, calculate the forward 10-day SMA of the high prices starting the next day
data['Forward_SMA10_High'] = data['Shifted_High'].rolling(window=10).mean().shift(-9)

# Calculate the percent change from the closing price on the day of the new high to the forward SMA10 high
data['Percent_Change_SMA_to_Close'] = ((data['Forward_SMA10_High'] / data['Adj Close'] - 1) * 100)

# Now filter to show only the rows where 'Is_New_High' is True
filtered_data = data[data['Is_New_High']]

# Calculate the standard deviation of the Percent_Change_SMA_to_Close for all new high days
std_deviation = filtered_data['Percent_Change_SMA_to_Close'].std()

print("Standard Deviation of Percent Change SMA to Close:", std_deviation)
print(filtered_data[['Adj Close', 'High', '52_Week_High', 'Is_New_High', 'Forward_SMA10_High', 'Percent_Change_SMA_to_Close']])
