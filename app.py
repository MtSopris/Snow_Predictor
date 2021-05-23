from flask import Flask, request, jsonify
# sqlalchemy
# can upload information with credentials - I can access this db with credentials, any data we put into db is now available into 

# heroku



app=Flask(__name__)



@app.route('/')
def index():
    return('Welcome to the home page')



@app.route('/predict')
def predict():
# use sqllite to access station names and latlongs 
    # grab input from form (or have user go to endpoint on their own)

    # loop over all possible stations, running our model on that input and each station
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
    dummy_output={

    }
    return jsonify({'input'})



if __name__=='__main__': 
	app.run()






