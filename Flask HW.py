import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs")

#Return Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
def precipitation():
    results = session.query(Measurement.prcp, Measurement.date).all()

    all_results = []
    for prcp in results:
        results_dict = {}
        station_dict['Measurement.station'] = station
        precipitation_dict['Measurement.prcp'] = precipitation
        dat_dict['Measurement.date'] = date
        all_results.append(results_dict)

    return jsonify(all_results)
        

#Return a JSON list of stations from the dataset.
def station():
    return jsonify(Measurement.station)

# Query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
if __name__ == "__main__":
    app.run(debug=True)