from flask import Flask, request, jsonify, render_template, redirect
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import json
from datetime import date, datetime
from sqlalchemy.orm import Session
import pickle

# load the previously persisted ML assets
with open('static/py/d_tree_range_modle_4.sav', 'rb') as f: 
    d_tree=pickle.load(f)

# connect to aws database
db_connection_string='postgresql://myPostgresDB:postgres@database-1.cmqf4nuaacji.us-east-2.rds.amazonaws.com:5432/postgres'

# establish session
engine = create_engine(db_connection_string)
Base=automap_base()
Base.prepare(engine, reflect=True)
User_Info=Base.classes.user_info
session=Session(engine)

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # get timestamp of click
    now = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    # get value of input data from form
    input_date=request.form['trip-start']
    zip_code=request.form['zip_code']
    dream=request.form['dream']
    planned=request.form['planned']
    activity=request.form['activity']
    # print(f'zip {zip_code}')
    # print(now)
    # print (input_date)
    # print(current_time)
    
    # # inserting click data into db
    # create a dictionary of click data
    new_input={'utc_now': now,
               'input_date': input_date,
               'zip_code': zip_code, 
               'dream': dream, 
               'planned': planned, 
               'activity': activity}

    # store new_input as a record in user_info table in database
    session.add(User_Info(**new_input)) #User_Info(utc_now=now, input_date=input_date, '...)
    session.commit()
  
    # turn input_date into day of year for ML model (1-366 value)
    yyyy, mm, dd = input_date.split("-")
    date_val = date(int(yyyy), int(mm), int(dd))
    day_of_year = date_val.strftime('%j')
    # print(request.form)

    # query historical database based on user chosen search date
    resultproxy = engine.execute(f'SELECT * FROM snow_means_table where dates={day_of_year}')

    # Create ML input array with historical values based on the date
    # create a blank array where we will append a dict for each station 
    output_array=[]
    return_json={'type': 'FeatureCollection', 
                 'features': []}
    for rowproxy in resultproxy:
        # print(rowproxy.items)

        # pulling relevant values for machine learning model
        input_array=[]
        row_array=rowproxy.values()

        # ML input does not include station name, change in snow depth, lat or long
        input_array=row_array[1:5]+row_array[6:8]+row_array[10:]
        # print(len(input_array))
 

        # pulling relevant values for final json object
        station_name=row_array[0]
        lat=row_array[8]
        lon=row_array[9]
        elevation=row_array[6]
        # print(f'input_array {input_array}')
        # print(station_name)
        # print(lat)
        # print(lon)

     
        # feed input array through ml model

        # pass input array through machine learning model 
        output=d_tree.predict([input_array])
        # print(f'station:{station_name} , input: {input_array}, output:{output}')

        # Create dictionary object with prediction and relevant station info
        station_dict={'type': 'Feature',  
                      'properties': {'station_name': station_name, 
                                     'day_of_year': input_array[0], 
                                     'predicted_snow': output[0], 
                                     'elevation': elevation},
                        'geometry': {'type': 'Point', 
                                     'coordinates': [lon,lat]}}

        # station_dict = {"station_name":station_name,
        #                 "day_of_year":input_array[0],
        #                 "predicted_snow": output[0], 
        #                 "lat": lat,
        #                 "lon": lon,
        #                 "elevation": elevation}
        # print(station_dict)

        # append station dict to output array
        return_json['features'].append(station_dict)


    print('Machine learning prediction complete')

    # write json object (list of station dictionaries) to file
    with open('static/output/ml_predict_output.json', 'w') as outfile:
        # json.dump(output_array, outfile)
        json.dump(return_json, outfile)


    # redirect user back to index.html for viewing map populated with ML output
    return redirect("/", code=302)

# If we wanted to add another route with sample user data 
# @app.route("/deep", methods = ['GET', 'POST'])
# def data_collection():
    
    

if __name__=='__main__': 
	app.run()






