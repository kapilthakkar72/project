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
from decimal import *

def getMandisForCentre(centre):
	query = "select mandicode from mandis where centreid = " + str(centre)
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	conn = psycopg2.connect(conn_string) 
	cursor = conn.cursor()
	cursor.execute(query)  
	records = cursor.fetchall()
	result = []
	for rec in records:
		result.append(rec[0])
	conn.close()
	return result

def getWP(mandi,start_date,period_months):
	result = []
	for i in range(0,period_months * 30):
		query = "select avg(modalpricersqtl) ws from wholesaleoniondata where mandicode= "+ str(mandi) +" and dateofdata<='"+str(start_date)+"' and dateofdata>= date '"+str(start_date)+"'-interval '6 day'";
		conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
		conn = psycopg2.connect(conn_string) 
		cursor = conn.cursor()
		cursor.execute(query)  
		records = cursor.fetchall()
		if(len(records) > 0):
			result.append((start_date,records[0][0]))
		start_date = start_date + relativedelta(days=1)
		conn.close()
	return result

def correlation(price1,price2):
    meanPrice1 = np.mean(price1)
    meanPrice2 = np.mean(price2)
    print "print correlation"

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

    return max,float(lag[index])

def insertToDB(date,centre,m1,m2,corr,lag, period_months):
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	conn = psycopg2.connect(conn_string) 
	cursor = conn.cursor()
	query = "INSERT INTO WPCorrAmongMandis(dateofdata,centreid,mandicode1,mandicode2,correlation,lag,period_months) VALUES ( '" + str(date) + "', "+ str(centre) + " , " + str(m1) + " ," + str(m2) +" , " + str(corr) + " , " + str(lag) +" , " + str(period_months) + ")" 
	cursor.execute(query)  
	conn.commit()
	conn.close()

if __name__ == "__main__":

	# Centre into consideration
	centres = [44,16,3,27,5,7,10,11,15,23,28,31,32,37,40,41,44,50,54,56,62,68]
	period_months = 2

	for centre in centres:
		# For each centre get the mandis and their prices
		mandis = getMandisForCentre(centre)

		# print "Got mandis for centre : " + str(centre)

		for m1 in mandis:
			for m2 in mandis:
				if(m1 != m2):
					# Go for date-wise... Period of 2 months, same as done previously

					StartDate = "01/07/06"
					EndDate = "05/31/15"

					start_date = datetime.datetime.strptime(StartDate, "%m/%d/%y")
					end_date = datetime.datetime.strptime(EndDate, "%m/%d/%y")

					while (start_date < end_date):
						wp10 = getWP(m1,start_date,period_months)  # [(date,price (avg of last 7 days))]
						wp20 = getWP(m2,start_date,period_months)	# [(date,price (avg of last 7 days))]

						# Join wp1 and wp2

						#print "Got wp10 and wp20 ... date : " + str(start_date)

						# Extracting arrival and wp
						wp1 = []
						wp2 = []
						joinedDate = []

						for rec1 in wp10:
							for rec2 in wp20:
								if(str(rec1[1]) == "None" or str(rec2[1]) == "None"):
									continue
								if(rec1[0].month == rec2[0].month and rec1[0].day == rec2[0].day):
									joinedDate.append(rec1[0])
									wp1.append(rec1[1])
									wp2.append(rec2[1])

						#print "joined...."

						# print "wp1"
						# print wp1
						# print "wp2"
						# print wp2

						if(len(wp1) == 0):
							start_date  = start_date + relativedelta(months = period_months)
							continue

						wp1 = np.array(wp1,dtype = float)
			    			wp2 = np.array(wp2,dtype = float)
			    			(corr,lag) = correlation(wp1,wp2)

			    			# print "Got correlation"
			    			insertToDB(start_date,centre,m1,m2,corr,lag,period_months)
			    			print str(start_date) + " "+ str(centre) + " " + str(m1)  + " " +str(m2) + " " + str(corr) + " " + str(lag)
			    			start_date  = start_date + relativedelta(months = period_months)