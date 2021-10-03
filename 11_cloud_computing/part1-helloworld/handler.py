import json
#typical python script


def hello(event, context):
    #this is the function we specify in serverless.yml
    #it takes two arguments (by design from AWS!)

    # event specifies how lambda was triggered and parameters to it
    body = {
        "message": "Go Serverless v1.0! Go IES JEM207 course! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response