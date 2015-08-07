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

def getMeRelativeDiff(date,centre,period_months):
    result = []
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    for i in range(0,30*period_months):
        query = "select avg(modalpricersqtl) from wholesaleoniondata w, mandis m where m.mandicode = w.mandicode and m.centreid = " + str(centre) + " and dateofdata = '" + str(date) + "'"
        cursor.execute(query)
        wp_rec = cursor.fetchall()
        query = "select price from retailoniondata where centreid =  " + str(centre) + " and dateofdata = '" + str(date) + "'"
        #print query
        cursor.execute(query)
        rp_rec = cursor.fetchall()
        #print i
        #print wp_rec
        #print rp_rec
        date = date + relativedelta(days = 1)
        if(len(rp_rec) < 1 or len(wp_rec) < 1 or wp_rec[0][0] == decimal.Decimal("0") or rp_rec[0][0] == decimal.Decimal("0")):
            continue
        if(str(wp_rec[0][0]) == "None" or str(rp_rec[0][0]) == "None"):
            continue
        relative_diff = (rp_rec[0][0] - wp_rec[0][0]) / wp_rec[0][0]*100;
        relative_diff = float(str(relative_diff))
        result.append((date,relative_diff))
    conn.close()
    return result

def insertToTable(date,centre,corr,lag):
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
    conn = psycopg2.connect(conn_string) 
    cursor = conn.cursor()
    query = "INSERT INTO relativediffcorr(dateofdata,centreid,correlation,lag,period_months) VALUES ( '" + str(date) + "', "+ str(centre) +" , " + str(corr) + " , " + str(lag) +" , " + str(period_months) + ")" 
    cursor.execute(query)  
    conn.commit()
    conn.close()

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
    	print str(r)
    	corr.append(r)
    	lag.append(delay)

    max = -2
    index = -1
    for i in range(0,len(corr)):
    	if(max < corr[i]):
    		max = corr[i]
    		index = i;

    return (max,float(lag[index]))

if __name__ == "__main__":
    centres = [44,16,3,27,5,7,10,11,15,23,28,31,32,37,40,41,44,50,54,56,62,68]
    period_months = 2
    for centre in centres:
        # For each centre we need to get retail, wholesale and date
        StartDate = "01/07/07"
        EndDate = "05/31/15"
        start_date = datetime.datetime.strptime(StartDate, "%m/%d/%y")
        end_date = datetime.datetime.strptime(EndDate, "%m/%d/%y")
        
        while(start_date < end_date):
            thisYearData = getMeRelativeDiff(start_date,centre,period_months)
            lastYearDate = start_date - relativedelta(years = 1)
            lastYearData = getMeRelativeDiff(lastYearDate,centre,period_months)
            
            #print thisYearData
            #print lastYearData
            
            # Merge Both data
            # Extracting arrival and wp
            realtiveDiff1 = []
            realtiveDiff2 = []
            joinedDate = []

            for rec1 in thisYearData:
                for rec2 in lastYearData:
                    if(str(rec1[1]) == "None" or str(rec2[1]) == "None"):
                            continue
                    if(rec1[0].month == rec2[0].month and rec1[0].day == rec2[0].day):
                        joinedDate.append(rec1[0])
                        realtiveDiff1.append(rec1[1])
                        realtiveDiff2.append(rec2[1])
            
            (corr,lag) = correlation(realtiveDiff1,realtiveDiff2)
            
            insertToTable(start_date,centre,corr,lag)
            
            start_date = start_date + relativedelta(months= period_months)