# SQLAlchemy Challenge

In preparation for a long holiday in Honolulu, Hawaii, I have decided to do some climate analysis on the area. 

## Step 1 - Climate Analysis and Exploration

To begin, I used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. All of the following analysis was completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Precipitation Analysis

* The most recent date in the data set was identified.

* Using this date, the last 12 months of precipitation data was retreived by querying the 12 preceding months of data.

* The query results were loaded into a Pandas DataFrame and the date column was set as the index.

* The results were ploted as seen below:

  ![prcp.png](https://github.com/kflores56/sqlalchemy-challenge/blob/main/prcp.png)

* Summary statistics for the precipitation data is seen here:

![summary_statistics.png](https://github.com/kflores56/sqlalchemy-challenge/blob/main/summary_statistics.png)

### Station Analysis

* A query was designed to calculate the total number of stations in the dataset.

* A query was designed to find the most active stations

* Using the most active station, the lowest, highest, and average temperatures were calcuated

* A query was designed to retrieve the last 12 months of temperature observation data and the results were ploted as a histogram.

![temp.png](https://github.com/kflores56/sqlalchemy-challenge/blob/main/temp.png)

## Step 2 - Climate App

After completing the initial analysis, a Flask API was designed based on the queries developed above. 

### Routes

* `/`
  * Home page.
  * Lists all routes that are available.

* `/api/v1.0/precipitation`
  * Lists all dates and precipiation 

* `/api/v1.0/stations`
  * Lists all stations

* `/api/v1.0/tobs`
  * Lists busiest station data

* `/api/v1.0/<start>` and `/api/v1.0/<start>,<end>`
  * Return list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

