import json
from data import download_daily_data
import numpy as np

def rebalance(event, context):

    #something ahppens
    print(event)

    jsbody = json.loads(event['body']) #if no body is given, load the empty string json
    tickers = jsbody.get('tickers',[]) #if there is payload with tickers


    df = download_daily_data(tickers)
    print(df)

    weights = calculate_portfolio(df)



    response = {
        "statusCode": 200,
        "body": json.dumps({"portfolio":weights})
    }

    return response



def calculate_portfolio(prices):
    log_ret = np.log(prices/prices.shift(1))
    cov_mat = log_ret.cov()
    cov_mat_inv = np.linalg.inv(cov_mat)

    unit_vector = np.ones(prices.shape[1])#unit vector, length is the number of tickers

    # w = inv_sigma*unit/(unit*inv_sigma*unit)

    w = np.dot(cov_mat_inv, unit_vector)/np.dot(np.dot(unit_vector, cov_mat_inv), unit_vector)

    return dict(zip(prices.columns, w)) #join names of tickers and their weights
