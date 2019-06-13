''' https://www.datacamp.com/community/tutorials/finance-python-trading '''
import pandas_datareader as pdr
import pandas as pd
import datetime 
import numpy as np



def model_function(signals,short_window):
        ''' Normally with > '''
        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                                    > signals['long_mavg'][short_window:], 1.0, 0.0) 
        return signals



    

for year in range(2010,2019,1):
        best_bank = 0
        count = 0

        print("\nGet Data for",year)

        asset = pdr.get_data_yahoo('BTC-USD', 
                                  start=datetime.datetime(year, 1, 1), 
                                  end=datetime.datetime(year+1, 1, 1))        
        print("Run Model")
        for short_window in range(1,51):
            for long_window in range(1,53):


                # Initialize the `signals` DataFrame with the `signal` column
                signals = pd.DataFrame(index=asset.index)
                signals['signal'] = 0.0

                # Create short simple moving average over the short window
                signals['short_mavg'] = asset['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

                # Create long simple moving average over the long window
                signals['long_mavg'] = asset['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

                # Create signals
                model_function(signals,short_window)
        #        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
        #                                                    < signals['long_mavg'][short_window:], 1.0, 0.0)   



                # Generate trading orders
                signals['positions'] = signals['signal'].diff()

                # Print `signals`
                #print(signals)





                # BACKTESTING

                # Set the initial capital
                initial_capital= float(100000.0)

                # Create a DataFrame `positions`
                positions = pd.DataFrame(index=signals.index).fillna(0.0)

                # Buy a 100 shares
                positions['BTC-USD'] = 100*signals['signal']   

                # Initialize the portfolio with value owned   
                portfolio = positions.multiply(asset['Adj Close'], axis=0)

                # Store the difference in shares owned 
                pos_diff = positions.diff()

                # Add `holdings` to portfolio
                portfolio['holdings'] = (positions.multiply(asset['Adj Close'], axis=0)).sum(axis=1)

                # Add `cash` to portfolio
                portfolio['cash'] = initial_capital - (pos_diff.multiply(asset['Adj Close'], axis=0)).sum(axis=1).cumsum()   

                # Add `total` to portfolio
                portfolio['total'] = portfolio['cash'] + portfolio['holdings']

                # Add `returns` to portfolio
                portfolio['returns'] = portfolio['total'].pct_change()

                # Print the first lines of `portfolio`
                #print(portfolio.head())
                #print(portfolio.tail())

                # Access last value of total in pandas dataframe. This is what needs to be optimized.
                total_now = portfolio['total'][-1]

                if total_now > best_bank:
                    best_bank = total_now
                    count +=1
                    print("Count,Short AVG,Long AVG,Best Bank",count,short_window,long_window,best_bank)
                    best_short_window = short_window
                    best_long_window = long_window

        print("HODL Gains:",asset['Adj Close'][-1] / asset['Adj Close'][1])            





quit()

long_window = best_long_window
short_window = best_short_window

# Initialize the `signals` DataFrame with the `signal` column
signals = pd.DataFrame(index=asset.index)
signals['signal'] = 0.0

# Create short simple moving average over the short window
signals['short_mavg'] = asset['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create long simple moving average over the long window
signals['long_mavg'] = asset['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Create signals
model_function(signals,short_window)


#signals['signal'] = np.where(signals['short_mavg'] 
#                                            > signals['long_mavg'], 1.0, 0.0) 

# Generate trading orders
signals['positions'] = signals['signal'].diff()

# Print `signals`
print(signals)


# Import `pyplot` module as `plt`
import matplotlib.pyplot as plt

# Initialize the plot figure
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111,  ylabel='Price in $')

# Plot the closing price
asset['Close'].plot(ax=ax1, color='r', lw=2.)

# Plot the short and long moving averages
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index, 
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='m')
         
# Plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index, 
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='k')
         
# Show the plot
plt.show()


# BACKTESTING

# Set the initial capital
initial_capital= float(100000.0)

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy a 100 shares
positions['BTC-USD'] = 100*signals['signal']   
  
# Initialize the portfolio with value owned   
portfolio = positions.multiply(asset['Adj Close'], axis=0)

# Store the difference in shares owned 
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(asset['Adj Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(asset['Adj Close'], axis=0)).sum(axis=1).cumsum()   

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

# Print the first lines of `portfolio`
print(portfolio.head())
print(portfolio.tail())


print("Portfolio Plot")
# Create a figure
fig = plt.figure()

ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

# Plot the equity curve in dollars
portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index, 
         portfolio.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(portfolio.loc[signals.positions == -1.0].index, 
         portfolio.total[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Show the plot
plt.show()


# SHARPE RATIO

# Isolate the returns of your strategy
returns = portfolio['returns']

# annualized Sharpe ratio
sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

# Print the Sharpe ratio
print("Sharpe Ratio",sharpe_ratio)


# DRAWDOWN

# Define a trailing 252 trading day window
window = 252

# Calculate the max drawdown in the past window days for each day 
rolling_max = asset['Adj Close'].rolling(window, min_periods=1).max()
daily_drawdown = asset['Adj Close']/rolling_max - 1.0

# Calculate the minimum (negative) daily drawdown
max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

# Plot the results
daily_drawdown.plot()
max_daily_drawdown.plot()

# Show the plot
plt.title("Drawdown")
plt.show()


# Compound Annual Growth Rate (CAGR)
# Get the number of days in `asset`
days = (asset.index[-1] - asset.index[0]).days

# Calculate the CAGR 
cagr = ((((asset['Adj Close'][-1]) / asset['Adj Close'][1])) ** (365.0/days)) - 1

# Print the CAGR
print("Compound Annual Growth Rate (CAGR)",cagr)

# What if I HODL'd
print("HODL Gains:",asset['Adj Close'][-1] / asset['Adj Close'][1])

