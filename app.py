from flask import Flask, request, jsonify, render_template
import sqlalchemy
from sqlalchemy import create_engine
import json
from datetime import date
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
    print(input_date)
    yyyy, mm, dd = input_date.split("-")
    print(yyyy)
    date_val = date(int(yyyy), int(mm), int(dd))
    day_of_year = date_val.strftime('%j')
    print(day_of_year)


    # with open (csvfile, 'w')
    # return ('prediction from user input here')
# use database to access station names and latlongs ->station route does this
    # /station returns list of dicts, each dict is station/elevation/lat/long
    resultproxy = engine.execute('SELECT * FROM station_means_table')
    # date = day_of_year

    d, a = {}, []
    # input_array=[]
    for rowproxy in resultproxy:
        # print(rowproxy['dates'])
        if rowproxy['dates']==int(day_of_year):
            # print('found it')
            input_array=[]
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            # print(rowproxy['station_name'])
            sn=rowproxy['station_name']
            # can add all other variables here. 
            sd_sod=rowproxy['snow_depth_start_of_day']# 'Snow Depth (in) Start of Day Values'
            # print(f'snow depth {sd_sod}')
            air_temp=rowproxy['air_temp_avg']# 'Air Temperature Observed (degF) Start of Day Values'
            # print(f'air temp {air_temp}')
            swq_sod= rowproxy['snow_water_equiv_start_of_day']
            # print(f'snow water {swq_sod}')
            input_array.append(day_of_year)
            input_array.append(sd_sod)
            input_array.append(air_temp)
            input_array.append(swq_sod)
            # input_array.append(sn)
            
            
            

            # print(input_array)
            # feed variables through ml model

            scaled_input=scaler.transform([input_array])
            print(scaled_input)
            # output=knn.predict(scaled_input)
        

        
        # if snow, 


        # for column, value in rowproxy.items():
        #     # check if snow with model 
        #     # if yes, build up the dictionary with snow values
        #     snow='yes'
        #     if snow =='yes':
        #         d ={**d, **{column: value}}
        # a.append(d)
        # write to output file
    # print(a)

    # save snow dictionary 
    return render_template('form.html') # add the html that is linked to js and will display visuals

    



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

    # save to json file
    return jsonify(a)
    


if __name__=='__main__': 
	app.run()






