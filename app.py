import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query all prcp
    results = session.query(Measurement).all()

    # Convert list of tuples into dictionary
    date_dict = []
    for x in results:
        prcp_dict = {}
        prcp_dict["date"] = x.date
        prcp_dict["prcp"] = x.prcp
        date_dict.append(prcp_dict)

    return jsonify(date_dict)


@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.name).all()
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results=session.query(Measurement).filter(Measurement.date>=year_ago).order_by(Measurement.date).all()
    date_dict = []
    for x in results:
        tobs_dict = {}
        tobs_dict["date"] = x.date
        tobs_dict["tobs"] = x.tobs
        date_dict.append(tobs_dict)

    return jsonify(date_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    results=session.query(Measurement.tobs).filter(Measurement.date>=start).order_by(Measurement.date).all()
    df = pd.DataFrame(results)
    TMIN=df["tobs"].min()
    TMAX=df["tobs"].max()
    TAVG=round(df["tobs"].mean(),1)

    temps={"start_date":start, "min_temp":TMIN,"max_temp":TMAX, "avg_temp":TAVG}
    
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    results=session.query(Measurement.tobs).filter(Measurement.date>=start).filter(Measurement.date<end).order_by(Measurement.date).all()
    df = pd.DataFrame(results)
    TMIN=df["tobs"].min()
    TMAX=df["tobs"].max()
    TAVG=round(df["tobs"].mean(),1)

    temps={"start_date":start, "end_time":end, "min_temp":TMIN,"max_temp":TMAX, "avg_temp":TAVG}
    
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)
