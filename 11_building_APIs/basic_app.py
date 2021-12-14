import time

import flask  # load flask library

app = flask.Flask(__name__)
# instantiate class "Flask"
# __name__ is a special variable that tells the app where to look for resources.


@app.route("/")  # this says that I want to register a view function for the given route
def index():
    return {  # Python dictionary will be automatically returned as json
        'response': 'Welcome to our first API',
        'version': '0.1',
        'support': 'kalab.frantisek@operatorict.cz'
    }


@app.route("/html")
def html():
    return "<p>Hello, World!</p>"  # I can easily return an HTML page


# Good practice is to expose a route where API users can check if your service is running
# It can contain other information, for example the status of your database etc.
@app.route("/healthcheck")
def healthcheck():
    return {
        'status': 'success',
        'timestamp': time.time()
        }
# I can check http code and body with: curl -v http://127.0.0.1:5000/healthcheck


# Three ways that a user can provide input
# Aruments to a get request
@app.route('/userinput-get', methods=['GET'])
def parse_get_request():
    return {'user_input': flask.request.args}


# Aruments to a get request -- dynamic routes TODO
@app.route('/userinput-get/<name>', methods=['GET'])
def parse_get_request_dynamic_url(name):
    return {'user_input': name}


# Body of a post request
# This is the go-to method for larger amounts of data
# It can also be safer, because no data is visible in the URL
@app.route('/userinput-post', methods=['POST'])
def parse_post_request():
    return {'user_input': flask.request.json}


# The following says:
# "if you call this program directly as python app.py, run the flask api"
# => if someone imported this file as a dependency, the api would not start.
if __name__ == '__main__':
    app.run()
