# Snow_Predictor 


Powder Hounds is an app that allows web users to explore future and historical daily snowfall throughout Colorado.

This app utilizes machine learning to generate a prediction of daily snow fall for 115 station throughout Colorado. The flask app accepts a date to generate a prediction from a decision tree machine learning model and aws rds database based on historical data.


## Visualizations

1. Heat Map - Displays the predicted snowfall through all of Colorado

<image src='static\images\world_map.PNG' alt='world_map.PNG' style='height:500px; width: 600px;'/>

2. Interactive Bar Charts - Displays analisis of historical user input including there trip plans and activities desired for the given data inputed.

<image src='static\images\bar_charts.PNG' alt='cost_living.PNG' style='height:450px; width: 600px;'/>

3. Rolling Bar Chart - Displays the historical data thoughout a 20 year period. 

<image src='static\images\rolling_bar.PNG' alt='year_in_out.PNG' style='height:400px; width: 600px;'/>



## Installing Dependencies

To install <Snow_Predictors>, the following libraries will be needed:


[Python](https://docs.python.org/3/)

[Matplotlib](https://matplotlib.org/)

[Numpy](https://numpy.org/doc/)

[Pandas](https://pandas.pydata.org/docs/)

[Sqlalchemy](https://docs.sqlalchemy.org/en/14/)

[SkLearn](https://scikit-learn.org/stable/)

[Datetime](https://docs.python.org/3/library/datetime.html)

[Psycopg2](https://pypi.org/project/psycopg2/)

[Flask](https://flask.palletsprojects.com/en/2.0.x/)

A [Mapbox](https://docs.mapbox.com/help/getting-started/) api key will need to be added to a config file with API_KEY as a variable file should be located in ../static/config/config.js


## Contributors

Thanks to the following people who have contributed to this project:


* [Anna Sours](https://github.com/acsours)
* [Erich Mitchell](https://github.com/Mitchemoto)
* [Spencer Davis](https://github.com/SMDavis19)
* [TJ Ossola](https://github.com/MtSopris)
* [Lisa Caruana](https://github.com/LisaCaruana)
* [Jason Sheridan](https://https://github.com/jxs5077)
* [Bailey Taber](https://https://https://github.com/bgtaber)



## Resources

[Natural Resources Conservation Services](https://wcc.sc.egov.usda.gov/reportGenerator/edit/customMultipleStationReport/daily/start_of_period/state=%22CO%22%20AND%20network=%22SNTLT%22,%22SNTL%22%20AND%20element=%22SNWD%22%20AND%20outServiceDate=%222100-01-01%22%7Cname/0,0/name,stationId,WTEQ::value,WTEQ::delta,SNWD::value,SNWD::delta?fitToScreen=false)


[Amazon AWS](https://aws.amazon.com/console/)

