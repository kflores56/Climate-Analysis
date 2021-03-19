from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# # Create our session (link) from Python to the DB
# session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f'<a href="/api/v1.0/precipitation">Precipitation:<br/>/api/v1.0/precipitation</a><br/>'
        f"<br/>"
        f'<a href="/api/v1.0/stations">List of Stations:<br/>/api/v1.0/stations</a><br/>'
        f"<br/>"
        f'<a href="/api/v1.0/tobs">Temperatures over the last 12 months of busiest station:<br/>/api/v1.0/tobs</a><br/>'
        f"<br/>"
        f'<a href="/api/v1.0/yyyy-mm-dd">Temperature details from selected date (yyyy-mm-dd):<br/>/api/v1.0/yyyy-mm-dd</a><br/>'
        f"<br/>"
        f'<a href="/api/v1.0/yyyy-mm-dd,yyyy-mm-dd">Temperature details from date range (yyyy-mm-dd,yyyy-mm-dd):<br/>/api/v1.0/yyyy-mm-dd,yyyy-mm-dd</a><br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates & precipiataion"""
    # Query info
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

     # Create a dictionary from the row data and append to a list of all_passengers
    weather_data = []
    for date, prcp in results:
        weather_dict = {}
        weather_dict["Date"] = date
        weather_dict["Precipiataion"] = prcp
        weather_data.append(weather_dict)

    return jsonify(weather_data)

@app.route("/api/v1.0/stations")
def stations ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query info
    results = session.query(Station.station, Station.name).all()

    session.close()

    stations = []
    for station,name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temps ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Find date one year from most recent date
    querydate = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Identify the most active station
    most_active = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).first()

    # Query the last 12 months of temperature observation data for busiest station
    recent_most_active = (session.query(Measurement.date, Measurement.tobs)
                     .filter(Measurement.station == most_active[0])
                     .filter(Measurement.date > querydate)
                     .order_by(Measurement.date)
                     .all())

    all = []
    for date, tobs in recent_most_active:
        d_t = {}
        d_t['Date'] = date
        d_t['Temperature'] = tobs
        all.append(d_t)
    
    return jsonify(all)

@app.route('/api/v1.0/<start>')
def get_start(start):
    session = Session(engine)
    start_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    temp_data = []
    for min,avg,max in start_result:
        temp_dict = {}
        temp_dict["Minumin"] = min
        temp_dict["Average"] = avg
        temp_dict["Maximum"] = max
        temp_data.append(temp_dict)

    return jsonify(temp_data)

@app.route("/api/v1.0/yyyy-mm-dd,yyyy-mm-dd")
def start_end(start,end):
    session = Session(engine)
    start_end_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    start_end_data = []
    for min,avg,max in start_end_result:
        se_dict = {}
        se_dict["Minumin"] = min
        se_dict["Average"] = avg
        se_dict["Maximum"] = max
        start_end_data.append(se_dict)

    return jsonify(start_end_data)

if __name__ == '__main__':
    app.run(debug=True)