import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
Base = automap_base()
# reflect an existing database into a new model
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

@app.route("/")
def home():
    return (
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
        )

#Return Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():

    start_date = "2017-4-1"
    s_date = dt.datetime.strptime(start_date, '%Y-%m-%d')

    previous_date = start_date - relativedelta(years=1)

    results = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date > previous_date).all()

    last_date=list()
    last_prcp=list()
    count=0
    for x in results:
        count+1
        last_date.append(x.date)
        last_prcp.append(x.prcp)
        if count % 200 == 0 :
            print(x.date, x.prcp)

    prcp_dict={"Date": last_date, "Precipitation": last_prcp}

    return jsonify(prcp_dict)
        

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station).distinct().all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    station_temps = session.query(Measurement.tobs).\
        filter(Measurement.date > previous_date).all()
    return jsonify(station_temps)
    

@app.route("/api/v1.0/<start>/<end>")
def tempst(start,end):

    st_date_inp  = start
    end_date_inp = end
    
    try:
        st_date_conv =  dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
        
    except:
        print(" Invalid start date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. start = 2017-08-21")
        print("start date input: " + st_date_inp)
        print(" ")
        st_date_inp   = '2017-08-21'
        st_date_conv  = dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
        
    try:
        end_date_conv = dt.datetime.strptime(end_date_inp, '%Y-%m-%d')
    except: 
        print(" Invalid end date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default  end date = current date")
        print("end date input:" + end_date_inp)
        print(" ")
        end_date_conv = dt.datetime.today().strftime('%Y-%m-%d')

    
    print(st_date_conv, end_date_conv)
     
    Meas_temp_st = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                     filter(Measurement.date >= st_date_conv).\
                     filter(Measurement.date <= end_date_conv).\
                     all()
    return jsonify(Meas_temp_st)

@app.route("/api/v1.0/<start>")
def tempstartonly(start):
    
    st_date_inp  = start
    
    try:
        st_date_conv =  dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
    

    except:
        print(" Invalid start date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. start = 2017-08-21")
        print("start date input: " + st_date_inp)
        st_date_inp   = '2017-08-21'
        st_date_conv  = dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
        
    print(st_date_conv)
  
    Meas_temp_st = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                     filter(Measurement.date >= st_date_conv).\
                     all()
    return jsonify(Meas_temp_st)
    
if __name__ == "__main__":
    app.run(debug=True)