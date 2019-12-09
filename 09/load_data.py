import requests
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import *

def get_foursquare_data(query,loc,CLIENT_ID,CLIENT_SECRET,limit=100):
    url = 'https://api.foursquare.com/v2/venues/explore'

    fsquare_params = dict(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      v='20190912',
      ll=','.join([str(c) for c in loc]),
      query=query,
      limit=limit
    )
    data = requests.get(url=url, params=fsquare_params).json()
    
    
    def parseFoursquare(place):
        lat=place['venue']['location']['lat'],
        lng=place['venue']['location']['lng'],
        d= dict(
            id=place['venue']['id'],
            name=place['venue']['name'],
            lat=lat[0],
            lng=lng[0],
            address=place['venue']['location']['address'],
            distance_ies=place['venue']['location']['distance'],
            category=','.join([cat['name'] for cat in place['venue']['categories']]),
            geometry=Point(lng[0],lat[0]) 
        )
        return pd.Series(d)
    return gpd.GeoDataFrame([parseFoursquare(place) for place in data['response']['groups'][0]['items']],crs={'init': 'epsg:4326'})


def get_overpass_amenity(amenityType,bounds):
    overpass_url = "http://overpass-api.de/api/interpreter"

    def parseOverpass(element):
        d = element['tags']
        d['id'] = element['id']
        d['lat'] = element['lat']
        d['lon'] = element['lon']
        d['geometry'] = Point(element['lon'],element['lat'])
        return pd.Series(d)
    
    police_overpass_query = '''
        [out:json];
        node
          [amenity={}]
          ({}, {}, {}, {});
        out;
        '''.format(amenityType,bounds[1],bounds[0],bounds[3],bounds[2])
    req = requests.get(overpass_url, 
                            params={'data': police_overpass_query}).json()
    return gpd.GeoDataFrame([parseOverpass(el) for el in req['elements']],crs={'init': 'epsg:4326'})



def get_all_stops(GOLEMIO_API_KEY):
    stops_golemio_url = 'https://api.golemio.cz/v1/gtfs/stops'
    dfs = []
    for i in range(20):
        stops_params = dict(
            limit=1000,
            offset=i*1000
        )
        r = requests.get(stops_golemio_url,
                        params=stops_params,headers={'X-Access-Token':GOLEMIO_API_KEY})
        dfs.append(gpd.read_file(r.text))
    return pd.concat(dfs,sort=False)


def get_police_stations(loc,distance,GOLEMIO_API_KEY):
    police_golemio_url = 'https://api.golemio.cz/v1/municipalpolicestations/'
    police_params = dict(
        latlng=','.join([str(c) for c in loc]),
        range=distance
    )
    r = requests.get(police_golemio_url,
                    params=police_params,headers={'X-Access-Token':GOLEMIO_API_KEY})
    return gpd.read_file(r.text,crs={'init': 'epsg:4326'})
