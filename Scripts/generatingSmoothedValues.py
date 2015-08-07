from bottle import route, run, debug, template, request, static_file, error, get, post, response,  static_file, view
import requests
import psycopg2
import math
import numpy as np
from sklearn import cluster
import psycopg2
import sys
import pprint
import matplotlib.pyplot as plt
import decimal
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO
import matplotlib
import bottle
from scipy.stats.kde import gaussian_kde
from scipy.stats import norm
import scipy
from scipy.interpolate import UnivariateSpline
import scipy.stats as stats
import datetime

def smoothPrices_Arrivals(start_date,centreid):

	prices = []
	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	conn = psycopg2.connect(conn_string) 
	cursor = conn.cursor()

	EndDate = "06/26/15"
	end_date = datetime.datetime.strptime(EndDate, "%m/%d/%y")

	for i in range(0,3454):
		query = "select avg(rp) rs,avg(wp) ws,avg(arrival) ar from summary where centreid= "+ str(centreid) +" and dateofdata<='"+str(start_date)+"' and dateofdata>= date '"+str(start_date)+"'-interval '6 day'";

		cursor.execute(query)  

		#print "Row count:" + str(cursor.rowcount)
		rec = cursor.fetchall()

		if cursor.rowcount == 0 or str(rec[0][0]) == "None":
			#print "Hello"
			start_date = start_date + datetime.timedelta(days=1)
			continue;

		# Execute Query to insert smoothed data into table		

		if(math.isnan(rec[0][1]) or  math.isnan(rec[0][0]) or math.isnan(rec[0][2])):
			start_date = start_date + datetime.timedelta(days=1)
			continue;

		date_string = str(start_date)
		query = "INSERT INTO smoothed_data(dateofdata,centreid,wholesaleprice,retailprice,arrivalsintons) VALUES ( '"+ date_string[:10] + "'," + str(centreid) + "," + str(rec[0][1]) + "," + str(rec[0][0]) + "," + str(rec[0][2]) +" )"
		cursor.execute(query)  
		print str(start_date)
		start_date = start_date + datetime.timedelta(days=1)
		prices.append((rec[0][1],rec[0][2]))

		if(start_date > end_date):
			break;

	conn.commit()
	conn.close()

	return prices

if __name__ == "__main__":
    StartDate = "2006-01-07"
    centreid = 16
    start_date = datetime.datetime.strptime(StartDate, "%Y-%m-%d")
    smoothPrices_Arrivals(start_date,centreid)
    print "Code Execution Finished"