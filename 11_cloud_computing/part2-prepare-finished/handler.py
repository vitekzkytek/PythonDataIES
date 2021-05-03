import json
from data import download_daily_data
import numpy as np


#where to find logs? AWS CloudWatch
#https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=%252Faws%252Flambda%252Fpart2-prepare-finished-dev-hello

def calculatePortfolio(event, context):

    print(event)
    if event['body'] is None:
        return create_response(403, {"message":"No data supplied"})

    jsbody = json.loads(event['body']) #if no body is given, load the empty string json
    tickers = jsbody.get('tickers',[]) #if there is payload with tickers

    if not tickers:
        return create_response(403, {"message":"No tickers submitted"})

    df = download_daily_data(tickers)
    weights = calculate_portfolio(df)

    return create_response(200, weights)

def create_response(status_code, resp):
    return {
        "statusCode": status_code,
        "body": json.dumps(resp)
    }

def calculate_portfolio(prices):
    log_ret = np.log(prices/prices.shift(1))
    cov_mat = log_ret.cov()
    cov_mat_inv = np.linalg.inv(cov_mat)

    unit_vector = np.ones(prices.shape[1])#unit vector, length is the number of tickers

    # w = inv_sigma*unit/(unit*inv_sigma*unit)

    w = np.dot(cov_mat_inv, unit_vector)/np.dot(np.dot(unit_vector, cov_mat_inv), unit_vector)
    
    return dict(zip(prices.columns, w)) #join names of tickers and their weights

