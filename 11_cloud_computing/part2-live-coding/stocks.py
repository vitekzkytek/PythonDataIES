import yfinance as yf
import pandas as pd
import logging

def get_data(tickers):
    '''
        Returns a pandas dataframe with named columns of Close prices from yfinance
    '''
    output = {}
    for tick in tickers:
        #use tolist
        try:
            stock_data = get_data_for_ticker(tick)
            output[tick]= stock_data
        except ValueError:
            #in case ticker does not exist
            logging.warning(f'Non-existent ticker {tick}')
            continue
    #make this Pandas DF
    # print(output)
    return pd.DataFrame(output)

def get_data_for_ticker(tick):
    '''
        return array of Close prices
    '''
    temp_stock = yf.Ticker(tick)
    #YTD data
    hist = temp_stock.history()
    close_prices = hist.Close.tolist()
    if len(close_prices)<1:
        raise ValueError(f"No prices - {tick}")

    return close_prices
