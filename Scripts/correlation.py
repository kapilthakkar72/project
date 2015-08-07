'''
Script to calculate Mean and standard deviation

'''
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
from dateutil.relativedelta import relativedelta

# print "City" + "," + "Year" + "," + "Month" + "," + "Mean" + "," + "Standard Deviation"



def smoothPrices_Arrivals(start_date,centreid):

	result = []
	for i in range(0,61):
		# query = "select retailprice, wholesaleprice, arrivalsintons,dateofdata from smoothed_data where centreid=16 and dateofdata ='"+str(start_date)+"'";
		query = "select avg(rp) rs,avg(wp) ws,avg(arrival) ar from summary where centreid= "+ str(centreid) +" and dateofdata<='"+str(start_date)+"' and dateofdata>= date '"+str(start_date)+"'-interval '6 day'";
		# print query
		#Define our connection string
		conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
		conn = psycopg2.connect(conn_string) 
		cursor = conn.cursor()
		cursor.execute(query)  
		rec = cursor.fetchall()
		start_date = start_date + datetime.timedelta(days=1)
		if(len(rec) > 0):
			result.append((rec[0][1],rec[0][2]))

	# print "Prices"
	# print len(prices)
	return result

def correlation(price1,price2):
    meanPrice1 = np.mean(price1)
    meanPrice2 = np.mean(price2)

    sx = 0.0
    sy = 0.0

    for i in range(0,len(price1)):
    	sx = sx + (price1[i] - meanPrice1) * (price1[i] - meanPrice1)
    	sy = sy + (price2[i] - meanPrice2) * (price2[i] - meanPrice2)
    denom = math.sqrt(sx*sy)

    floatZero = 0.0
    if str(denom) == str(floatZero):
        return (-5.0,-5.0)

    maxdelay = 15
    corr = []
    lag = []

    for delay in range(-maxdelay,maxdelay) :
    	sxy = 0.0
    	for i in range(0,len(price1)):
    		j = i+ delay
    		if(j<0 or j>=len(price2)):
    			continue
    		else:
    			sxy = sxy + (price1[i] - meanPrice1) * (price2[j] - meanPrice2)


    	r = sxy / denom
    	# print str(r)
    	corr.append(r)
    	lag.append(delay)

    max = -2
    index = -1
    for i in range(0,len(corr)):
    	if(max < corr[i]):
    		max = corr[i]
    		index = i;
    		
    return [max,float(lag[index])]

def wholesale_correlation(price1,price2,lagi):
    meanPrice1 = np.mean(price1)
    meanPrice2 = np.mean(price2)
    sx = 0.0
    sy = 0.0

    for i in range(0,len(price1)):
    	sx = sx + (price1[i] - meanPrice1) * (price1[i] - meanPrice1)
    	sy = sy + (price2[i] - meanPrice2) * (price2[i] - meanPrice2)
    denom = math.sqrt(sx*sy)

    floatZero = float(0.0)

    if str(denom) == str(floatZero):
        return -5.0

    maxdelay = 15
    corr = []
    lag = []

    for delay in range(-maxdelay,maxdelay) :
    	sxy = 0.0
    	for i in range(0,len(price1)):
    		j = i+ delay
    		if(j<0 or j>=len(price2)):
    			continue
    		else:
    			sxy = sxy + (price1[i] - meanPrice1) * (price2[j] - meanPrice2)


    	r = sxy / denom
    	# print str(r)
    	
    	if delay == round(lagi):
    		return r
    	
    return -6


if __name__ == "__main__":

	centres = [44,16,3,27,5,7,10,11,15,23,28,31,32,37,40,41,44,50,54,56,62,68]
	
	for centre in centres:
	    StartDate = "01/07/07"
	    EndDate = "05/31/15"

	    start_date = datetime.datetime.strptime(StartDate, "%m/%d/%y")
	    end_date = datetime.datetime.strptime(EndDate, "%m/%d/%y")

	    while (start_date < end_date):    
		    array1=smoothPrices_Arrivals(start_date,centre)

		    last_year = start_date - relativedelta(years=1)

		    array2=smoothPrices_Arrivals(last_year,centre)
		    arrival1 = []
		    arrival2 = []


		    for i in range(0,len(array1)):
		    	if(str(array1[i][1]) == "None" or str(array2[i][1]) == "None"):
		    		continue
		    	if(math.isnan(float(str(array1[i][1]))) or math.isnan(float(str(array2[i][1])))):
		    		continue
		    	# print "Array 1 :"+str(array1[i][1])
		    	arrival1.append(array1[i][1])
		    	arrival2.append(array2[i][1])


		    arrival1 = np.array(arrival1,dtype = float)
		    arrival2 = np.array(arrival2,dtype = float)

		    # print "Arrival Correlation:"
		    max_arrival_corr = correlation(arrival1,arrival2)

            	    if(max_arrival_corr[0] < -4.0):
                	print "Denom Zero while calculating Arrival Correlation: Date:"+str(start_date) + " Centre:"+str(centre)
                	start_date = start_date + relativedelta(months = 2)
                	continue

	    	    if max_arrival_corr[0] > 0.5 :
			    wp1 = []
			    wp2 = []

			    for i in range(0,len(array1)):
			    	if(str(array1[i][0]) == "None" or str(array2[i][0]) == "None"):
			    		continue
			    	if(math.isnan(array1[i][0]) or math.isnan(array2[i][0])):
			    		continue
			    	# print "Array 1 :"+str(array1[i][1])
			    	wp1.append(array1[i][0])
			    	wp2.append(array2[i][0])

			    wp1 = np.array(wp1,dtype = float)
			    wp2 = np.array(wp2,dtype = float)

			    # print "Wholesale Correlation:"
			    lag = max_arrival_corr[1]
			    max_wholesale_corr = wholesale_correlation(wp1,wp2,lag)

             		    if(max_wholesale_corr < -4.0):
                    		print "Denom Zero while calculating Wholesale Correlation: Date:"+str(start_date) + " Centre:"+str(centre)
                    		start_date = start_date + relativedelta(months = 2)
                    		continue
					
			    if(max_wholesale_corr < 0):
			    	print "Yuppiiieee!!! FOUND ONE... : Centre:"+ str(centre) + " date: " + str(start_date) + " : "+ str(max_arrival_corr[0]) + " "+ str(max_wholesale_corr)

		    print str(centre) + " " + str(start_date)
		    start_date = start_date + relativedelta(months = 2)
