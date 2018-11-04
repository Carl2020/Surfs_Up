import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_, or_, not_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation measurements"""
    # Query all dates in the last 12 months and obtain precipitation measures
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(and_(Measurement.date<='2017-08-23', Measurement.date>='2016-08-23')).\
    order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = {date:prcp for date, prcp in results}
 
    return jsonify(all_dates)
 

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    results2 = session.query(Station.station).all()

       # Convert list of tuples into normal list
    all_stations = list(np.ravel(results2))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature readings"""
# Query to show temperature readings for the last 12 months filtered by the most active station
    results3 = session.query(Measurement.date, Measurement.tobs).\
    filter(and_(Measurement.date<='2017-08-18', Measurement.date>='2016-08-18', Measurement.station=='USC00519281')).\
    order_by(Measurement.date.desc()).all()


    # Create a dictionary from the row data and append to a list of all_temps
    all_dates2 = {date:tobs for date, tobs in results3}

    return jsonify(all_dates2)

  
@app.route("/api/v1.0/<start>")
def start():
    """Return a JSON list of the minimum, average and max temperatures for a given start date and thereafter to the end of the range of dates"""
# Request the user to provide a start date between the range of 2016-08-18 and 2017-08-18
    start = "%%%Y-%m-%d"
   
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= Measurement.date[len(Measurement.date)]).all())
    

@app.route("/api/v1.0/<start>/<end>")
def end():
    """Return a JSON list of the minimum, average and max temperatures for a given start and end range"""
# Request the user to provide a start and end date between the range of 2016-08-18 and 2017-08-18
    start = "%%%Y-%m-%d"
    end = "%%%Y-%m-%d"
   
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all())
    

if __name__ == '__main__':
    app.run(debug=True)
