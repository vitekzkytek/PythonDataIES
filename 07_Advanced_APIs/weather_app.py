import requests
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv


# read environment variables
load_dotenv()

# Specify which cities should be loaded by default
DEFAULT_CITIES = ['Prague', 'Berlin', 'Vienna']

# Setup 
UPDATE_DELAY = 10
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    desc = db.Column(db.String, nullable=False)
    icon = db.Column(db.String(50),nullable=False)
    last_updated  = db.Column(db.DateTime, nullable=False)

class WeatherRetrievalException(Exception):
    pass

def prepare_for_rendering(data_object, now):
    '''
    Converts the SQLAlchemy row object into a dictionary with minutes since last update and whether it is more than 10 minutes
    '''

    d = data_object.__dict__
    ago = round((now - d['last_updated']).total_seconds()/60)
    d['minutes_ago'] = ago
    d['update_warning'] = ago > UPDATE_DELAY
    return d


@app.route('/', methods=['GET'])
def index():
    '''
    Main page queries the cities in the database and displays it on jinja template
    '''

    # query the database
    cities = City.query.all()

    now = datetime.now()

    # compute update delays (see the function above)
    cities_for_rendering = [prepare_for_rendering(obj, now) for obj in cities]
    
    # render template
    return render_template('weather.html', cities=cities_for_rendering)


def parse_city_info(city):
    '''Downloads city name from OpenWeatherMap API and converts it into SQLAlchemy object'''
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={token}'

        r = requests.get(url.format(city=city,token=os.getenv('OPEN_WEATHER_API_TOKEN'))).json()

        return City(
            name=city,
            temp=r['main']['temp'],
            desc=r['weather'][0]['description'],
            icon=r['weather'][0]['icon'],
            last_updated=datetime.now()
        )
    except:
        raise WeatherRetrievalException(f'Could not retrieve data from OpenWeatherMap API in {city}')

@app.route('/add', methods=['POST'])
def add_city():
    '''
    Adds information about new city into the database
    '''
    new_city = request.form.get('city')

    if new_city:
        city_obj = parse_city_info(new_city)

        db.session.add(city_obj)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/default_cities', methods=['POST'])
def default_cities():
    '''
    Deletes all rows from database and downloads DEFAULT_CITIES
    '''
    db.session.query(City).delete()
    
    for city in DEFAULT_CITIES:
        city_obj = parse_city_info(city)
        db.session.add(city_obj)
    
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update_expired',methods=['POST'])
def update_expired():
    '''
    For cities which were not updated more than UPDATE_DELAY minutes ago, do the update
    '''
    cities = City.query.all()
    now = datetime.now()
    expired_cities = [city for city in cities if (now - city.last_updated) > timedelta(minutes=UPDATE_DELAY)]

    for city in expired_cities:
        db.session.delete(city)
        new_city = parse_city_info(city.name)
        db.session.add(new_city)
    db.session.commit()
    return redirect(url_for('index'))