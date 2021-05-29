from flask import Flask, request, jsonify, render_template, redirect
import sqlalchemy
from sqlalchemy import create_engine
import json
from datetime import date, datetime
import pickle

# load the previously persisted ML assets
with open('static/py/final_modle.sav', 'rb') as f: 
	knn=pickle.load(f)
with open('static/py/input_scaler.sav', 'rb') as f: 
	scaler=pickle.load(f)

# connect to heroku database
db_connection_string = "postgresql://mnaxahwxxlsupb:82ba661b23abc055281f8b75926dee77b960380953d91b0529fe16e0ed78f832@ec2-54-163-97-228.compute-1.amazonaws.com:5432/dajiaraierf0ld"

# I was using a test db on my local machine to try inserting files
# db_connection_string = 'postgresql://postgres:postgres@localhost:5432/testdb'
engine = create_engine(db_connection_string)


app=Flask(__name__)



@app.route('/')
def index():

    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # get value of input date from form
    input_date=request.form['trip-start']
    # get timestamp now
    now = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    # get zipcode from form
    zip_code=request.form['zip_code']
    dream=request.form['dream']
    planned=request.form['planned']
    activity=request.form['activity']
    # print(f'zip {zip_code}')
    # print(now)
    # print (input_date)
    # print(current_time)
    
    # # inserting click data into db

    # create string of SQL insert statement using user input from index.html
    # query = (f'INSERT INTO user_info (utc_now, input_date, zip_code) VALUES ({now}, {input_date}, {zip_code})')

    # execute query
    # engine.execute(str(query))
    

    #
    # print(input_date)
    yyyy, mm, dd = input_date.split("-")
    # print(yyyy)
    date_val = date(int(yyyy), int(mm), int(dd))
    day_of_year = date_val.strftime('%j')
    # print(day_of_year)

    resultproxy = engine.execute('SELECT * FROM station_means_table')

    output_array=[]
    for rowproxy in resultproxy:
        if rowproxy['dates']==int(day_of_year):
            # print('found it')
            input_array=[]
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            # print(rowproxy['station_name'])
            
            # pull variables for final json object
            station_name=rowproxy['station_name']
            lat=rowproxy['lat']
            lon=rowproxy['long']
            elevation=rowproxy['elevation']

            # pull variables for machine learning model input 
            sd_sod=rowproxy['snow_depth_start_of_day']# 'Snow Depth (in) Start of Day Values'
            # print(f'snow depth {sd_sod}')
            air_temp=rowproxy['air_temp_avg']# 'Air Temperature Observed (degF) Start of Day Values'
            # print(f'air temp {air_temp}')
            swq_sod= rowproxy['snow_water_equiv_start_of_day']
            # print(f'snow water {swq_sod}')
            input_array.append(int(day_of_year))
            # input_array.append(sd_sod)
            input_array.append(air_temp)
            input_array.append(swq_sod)
            # print(input_array)
            

            # feed variables through ml model
            scaled_input=scaler.transform([input_array])
            # print(scaled_input)
            output=knn.predict(scaled_input)
            # print(f'station:{sn} , input: {input_array}, output:{output}')

            # Create dictionary object with prediction and relevant info
            station_dict = {"station_name":station_name,
                            "predicted_snow": output[0], 
                            "lat": lat,
                            "lon": lon,
                            "elevation": elevation}

            output_array.append(station_dict)

    # print(output_array)
    # return jsonify(['hi'])
    # return jsonify(output_array)
    print('Machine learning prediction complete')
    # write json object to file
    with open('static/output/ml_predict_output.json', 'w') as outfile:
        json.dump(output_array, outfile)

    # print(output_array[0])
    return redirect("/", code=302)

# @app.route("/deep", methods = ['GET', 'POST'])
# def data_collection():
    
    

if __name__=='__main__': 
	app.run()






