from flask import Flask, request, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import json

# sqlalchemy
# can upload information with credentials - I can access this db with credentials, any data we put into db is now available into 

# heroku

db_connection_string = "postgres://mnaxahwxxlsupb:82ba661b23abc055281f8b75926dee77b960380953d91b0529fe16e0ed78f832@ec2-54-163-97-228.compute-1.amazonaws.com:5432/dajiaraierf0ld"
engine = create_engine(db_connection_string)
station_name_array=engine.execute('SELECT station_name FROM station_table').fetchall()
lat_lon=engine.execute('SELECT station_table.latitude, station_table.longitude FROM station_table').fetchall()

# stations=[]
# for each_station in station_name_array:
#     station=each_station[0]
#     stations.append(station)

# print(lat_lon)

app=Flask(__name__)



@app.route('/')
def index():
    # stations=[]
    # for each_station in station_name_array:
    #     station=each_station[0]
    #     stations.append(station)
    # print(f'first lat_lon {lat_lon[0]}')
    # print(f'first station {stations[0]}')
    return('Welcome to the home page')



@app.route('/predict')
def predict():

    # return ('prediction from user input here')
# use database to access station names and latlongs ->station route does this
    # /station returns list of dicts, each dict is station/elevation/lat/long
    resultproxy = engine.execute('SELECT * FROM station_table')

    d, a = {}, []
    for rowproxy in resultproxy:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d ={**d, **{column: value}}
        a.append(d)
    # print(a)
    
    for each_dict in a:
        # print(each_dict['station_name'])
        # run model with input date (comes from form)
        # store output in shape (dict) along with station 


    return ('done')
    # grab input from form (or have user go to endpoint on their own)
    # input = 100 (day of year)

    # loop over all possible stations, running our model on that input and each station
    # for each_station in lat_lon:
        # run model with input date (comes from form)

    # store output in shape (dict) along with station 
    # could optionally have list of lat longs that is stored here as well




    # loop through all possible lat longs in model, 
        # put latlongs into one value, as an array
        # code in model as onehot encoding

    # input_date
        # for each_stion in array of stations:
        #   plug into model with input date 
            # snowfall=intercept+date*b1+station*b2
            # b1, b2, respective weights of variables

    # here will be dictionary of the output coming from ml model 
    # stationnames 
    # latlongs with corresponding date and snowfall

    # final dictionary
    # what do we want final dict look like? -> how does leaflet want a heatmap?
    # dummy_output={
        # date
        # station_name: ,
        # lat_lon: ,
        #  elevation: ,
        # snowfall ,
        # date?

    # }
    # return jsonify({'input'})

@app.route('/stations')
def stations():


    resultproxy = engine.execute('SELECT * FROM station_table')

    d, a = {}, []
    for rowproxy in resultproxy:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d ={**d, **{column: value}}
        a.append(d)
    return jsonify(a)


if __name__=='__main__': 
	app.run()






