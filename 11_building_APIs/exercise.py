"""
You are the provider of healthcare statistics and want to expose an API that provides the daily information on new Covid-19 cases
Internally in your team, new cases are stored in an SQL database (we are using SQLite as an example)
Your data consumers want to always have the cases count for a single date that they ask for

Use the following code and fill the gaps to achieve the goal. Mind the comments for hints on how to proceed.
"""
import os
import time
import sqlite3

import flask
import pandas as pd


from dotenv import load_dotenv

app = flask.Flask(__name__)

# go to a file called .env-example, rename it to .env and replace XXXX with the full name of the sqlite file in this folder
# the files might apear as hidden, in your file browser make sure hidden files are shown
# this is a good way to supply connection strings and other secrets to your applications
load_dotenv()

# Add the two routes as they were shown before "/" giving basic information "/healthcheck" giving back api status


# Now create a route /infectionscount. 
# You can choose one of the three ways that the user can provide you with a date
@app.route(# to be filled in)
def get_infections_count():
    with sqlite3.connect(os.getenv('DB_CONNSTRING')) as con: #more on this later
        requested_date = # get date from user request, based on your chosen method
        # Now you can use pd.read_sql_query() to get data from your database
        # Example query: SELECT report_date, infected_count_daily FROM covid_infections_count WHERE report_date = '2021-05-01'
        return {'infected_count': #number of cases for the provided day}


# Now go ahead and run it. You can use the provided jupyter notebook to test that it works! 
if __name__ == '__main__':
    app.run()
