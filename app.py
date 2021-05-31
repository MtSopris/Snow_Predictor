from flask import Flask, request, jsonify, render_template, redirect
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import json
from datetime import date, datetime
from sqlalchemy.orm import Session
import pickle

# load the previously persisted ML assets
# with open('static/py/final_modle.sav', 'rb') as f: 
# 	knn=pickle.load(f)
# with open('static/py/input_scaler.sav', 'rb') as f: 
# 	scaler=pickle.load(f)
# with open('../rf_range_model_2.sav', 'rb') as f: 
#     rf=pickle.load(f)
with open('static/py/rf_range_model_3.sav', 'rb') as f: 
    rf=pickle.load(f)

# connect to aws database
db_connection_string='postgresql://myPostgresDB:postgres@database-1.cmqf4nuaacji.us-east-2.rds.amazonaws.com:5432/postgres'
# connect to heroku database
# db_connection_string = "postgresql://mnaxahwxxlsupb:82ba661b23abc055281f8b75926dee77b960380953d91b0529fe16e0ed78f832@ec2-54-163-97-228.compute-1.amazonaws.com:5432/dajiaraierf0ld"


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
     # get timestamp now
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
    session.add(User_Info(**new_input)) #User_Info(utc_now=now, input_date=input_date, '...)
    session.commit()
  
    # turn input_date into day of year for ML model (1-366 value)
    yyyy, mm, dd = input_date.split("-")
    date_val = date(int(yyyy), int(mm), int(dd))
    day_of_year = date_val.strftime('%j')
    # print(request.form)
    # resultproxy = engine.execute(f'SELECT * FROM station_means_full_list where dates={day_of_year}')
    resultproxy = engine.execute(f'SELECT * FROM snow_means_table where dates={day_of_year}')


    # create a blank array where we will append a dict for each station 
    output_array=[]
    for rowproxy in resultproxy:
        # print(rowproxy.items)

        # pulling relevant values for machine learning model
        input_array=[]
        row_array=rowproxy.values()

        # without change in snow depth
        input_array=row_array[1:5]+row_array[6:8]+row_array[10:]
        print(len(input_array))
        # includes change in snow depth
        # input_array=row_array[1:8]+row_array[10:23]
        # print(new_array)

        # pulling relevant values for final json object
        station_name=row_array[0]
        lat=row_array[8]
        lon=row_array[9]
        elevation=input_array[5]
        print(f'input_array {input_array}')
        # print(station_name)
        # print(lat)
        # print(lon)

     
        # feed input array through ml model

        # If using KNN model, must scale input array
        # scaled_input=scaler.transform([input_array])
        # print(scaled_input)

        # pass input array through machine learning model 
        output=rf.predict([input_array])
        # print(f'station:{sn} , input: {input_array}, output:{output}')
        print(f'ML output: {output}')

        # Create dictionary object with prediction and relevant station info
        station_dict = {"station_name":station_name,
                        "day_of_year":input_array[0],
                        "predicted_snow": output[0], 
                        "lat": lat,
                        "lon": lon,
                        "elevation": elevation}
        # print(station_dict)

        # append station dict to output array
        output_array.append(station_dict)

    # # return jsonify(['hi'])
    # # return jsonify(output_array)
    print('Machine learning prediction complete')

    # write json object (list of station dictionaries) to file
    with open('static/output/ml_predict_output.json', 'w') as outfile:
        json.dump(output_array, outfile)

    # print(output_array[0])

    # redirect user back to index.html for viewing heatmap
    return redirect("/", code=302)

# @app.route("/deep", methods = ['GET', 'POST'])
# def data_collection():
    
    

if __name__=='__main__': 
	app.run()






