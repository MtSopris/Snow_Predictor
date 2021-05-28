from flask import Flask, request, jsonify, render_template
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


db_connection_string = "postgres://mnaxahwxxlsupb:82ba661b23abc055281f8b75926dee77b960380953d91b0529fe16e0ed78f832@ec2-54-163-97-228.compute-1.amazonaws.com:5432/dajiaraierf0ld"
engine = create_engine(db_connection_string)


app=Flask(__name__)



@app.route('/')
def index():

    return render_template('form.html')
    # return render_template('index.html') index.html has dropdown that takes you to form 


@app.route('/predict', methods=['POST'])
def predict():
    input_date=request.form['trip-start']
    # now = datetime.now()
    # current_time=now.strftime("%H:%M:%S")
    #get time.now
    # get zipcode
    
    # inserting click data into db
    # engine.execute(f'INSERT into table VALUES ({input_date}, {time.now()},{zipcode})
    
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
            station_name=rowproxy['station_name']
            lat=rowproxy['lat']
            lon=rowproxy['long']
            elevation=rowproxy['elevation']

            # can add all other variables here. 
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

            station_dict = {"station_name":station_name,
                            "predicted_snow": output[0], 
                            "lat": lat,
                            "lon": lon,
                            "elevation": elevation}

            output_array.append(station_dict)

    # print(output_array)
    # return jsonify(['hi'])
    return jsonify(output_array)



if __name__=='__main__': 
	app.run()






