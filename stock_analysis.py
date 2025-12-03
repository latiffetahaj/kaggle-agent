
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create graphs directory if it doesn't exist
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# List of stocks to analyze
stocks_to_analyze = ['GOOGL', 'AAPL', 'AMZN']
dataset_folder = './datasets' #full path to the dataset folder

for stock_symbol in stocks_to_analyze:
    file_path = f"{dataset_folder}/stocks/{stock_symbol}.csv"
    
    if os.path.exists(file_path):
        # Read the dataset
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # --- Graph 1: Closing Price Over Time ---
        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['Close'], label='Close Price')
        plt.title(f'{stock_symbol} Closing Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'graphs/{stock_symbol}_closing_price.png')
        plt.close()

        # --- Graph 2: Moving Averages ---
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['Close'], label='Close Price', alpha=0.5)
        plt.plot(df['Date'], df['MA20'], label='20-Day Moving Average')
        plt.plot(df['Date'], df['MA50'], label='50-Day Moving Average')
        plt.title(f'{stock_symbol} Closing Price with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'graphs/{stock_symbol}_moving_averages.png')
        plt.close()

        # --- Graph 3: Trading Volume ---
        plt.figure(figsize=(12, 6))
        plt.bar(df['Date'], df['Volume'], label='Volume')
        plt.title(f'{stock_symbol} Trading Volume Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'graphs/{stock_symbol}_volume.png')
        plt.close()
