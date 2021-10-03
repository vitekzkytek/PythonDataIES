import yfinance as yf
import pandas as pd
import logging

def download_daily_data(tickers=['MSFT', 'FB','GOOG','GS','INTC', 'AAL', 'AAPL']):
    final_data = {}
    for ticker in tickers:
        logging.info(f'downloading data for {ticker}')
        td = yf.Ticker(ticker)
        hist_prices = td.history() #get last year of data
        final_data[ticker] = hist_prices.Close.tolist() #save Close prices as simple list

    return pd.DataFrame(final_data)