import json
from stocks import get_data
import numpy as np


def portfolio(event, context):
    '''
        Lambda entrypoint
    '''
    #lets get the json payload, validate the payload
    tickers = event['body'].get('tickers',[])
    if len(tickers)<2:
        return create_error(401, "Not enough tickers provided")
    #lets get data in pandas DF
    stock_data = get_data(tickers)
    #check resulting DF has at least 2 columns
    if stock_data.shape[1] < 2 :
        return create_error(401, "Not enough tickers data retrieved")
    #get weights
    weights = create_portfolio_for_close_prices(stock_data)

    response = {
        "statusCode": 200,
        "body": json.dumps({"tickers":stock_data.columns.tolist(),"weights":weights})
    }

    return response

def create_error(status,message):
    return {"statusCode":status, "message":message }

def create_portfolio_for_close_prices(df):
    '''
        using Close prices, get portfolio, return dict {ticker1:weight, ticker2:weight}
    '''

    #lets get returns - pandas DF

    ret = df.pct_change().dropna()
    cov_mat = ret.cov()
    cov_mat_inv = np.linalg.inv(cov_mat)
    unit_vector = np.ones(df.shape[1])#unit vector, length is the number of tickers
    w = np.dot(cov_mat_inv, unit_vector)/np.dot(np.dot(unit_vector, cov_mat_inv), unit_vector)
    # do properly
    # assert np.sum(w)==1, 'weights do not sum to one'
    return dict(zip(df.columns, w)) #join names of tickers and their weights


if __name__=="__main__":
    print('running script')
    payload = {
        "tickers":['MSFT','TSLA','AAPL','FDFF']
    }
    print(portfolio({
        "body":payload
    }, None))