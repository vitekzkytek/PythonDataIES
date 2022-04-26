import flask
from dotenv import load_dotenv

app = flask.Flask(__name__)
# instantiate class "Flask"
# __name__ is a special variable that tells the app where to look for resources.


# Load database connection as an ENVIRONMENT variable. 
# By defaults looks for `.env` file and reads its content.
# It is a good practice to include major config stuff as environmental variables
load_dotenv()

## Assign function to route
@app.route("/") 
def index():
    return '<h1>Hello World!</h1>'


# Good practice is to expose a route where API users can check if your service is running
# It can contain other information, for example the status of your database etc.
@app.route("/healthcheck")
def healthcheck():
    return {  # Python dictionary will be automatically returned as json
        'response': 'Welcome to our first API',
        'version': '0.1',
        'support': 'vitekzkytek@gmail.com'
    }


# You can translate route attributes to parameters and specify methods for which such method is allowed
@app.route('/introduction/<user>', methods=['GET'])
def get_message(user):
    return f'<h1>Hello World!</h1><p>This is <strong>{user}</strong> speaking...'




# The following says:
# "if you call this program directly as python app.py, run the flask api"
# => if someone imported this file as a dependency, the api would not start.
if __name__ == '__main__':
    app.run() 