# This file generates smooth data, exponential moving average with alpha =  2/15 ( 2 / (1+time_period) ).

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

alpha = 2.0/15.0

def smoothArray(dateofdata, array, end_date):
    array = np.array(array,dtype = float)
    start_date = "01/01/06"
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%y").date()
    
    new_data = []
    prevVal = -1
    
    i=0 # To keep track over the arrays passed
    while(start_date <= end_date):
        if(start_date == dateofdata[i]):
            # data for this date is present
            if(i==0):
                # Simply add to final array
                prevVal = array[i]
                new_data.append([start_date,array[i]])                
            else:
                # Smooth
                if(prevVal == -1):
                    prevVal = array[i]
                    new_data.append([start_date,array[i]])
                else:
                    newVal = ( array[i] - prevVal ) * alpha + prevVal
                    new_data.append([start_date,newVal])
                    prevVal = newVal
            start_date = start_date + datetime.timedelta(days=1)
            i = i+1 
        else:
            # Data for this date is missing
            
            if(prevVal == -1):
                new_data.append([start_date,array[i]])
            else:
                new_data.append([start_date,prevVal])            
            start_date = start_date + datetime.timedelta(days=1)    
    return new_data


def smoothPrices_Arrivals(centreid):
    
    query = "select dateofdata, coalesce(sum(ArrivalsInTons),0), coalesce(avg(ModalPriceRsQtl)/100,0) from wholesaleoniondata as w,mandis m where m.centreid = " + str(centreid) + " and  w.mandicode = m.mandicode group by dateofdata order by dateofdata;"
    
    
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(query)
    wholesaleRecords = cursor.fetchall()
    

    query = "select DateOfData,coalesce(Price,0) from RetailOnionData as r where r.centreid = "+ str(centreid) +" and extract(year from dateofdata) > 2005 order by DateOfData"
    cursor.execute(query)
    retailRecords = cursor.fetchall()
    
    if(not(len(wholesaleRecords) >1 and len(retailRecords) >1)):
        return
    
    if(wholesaleRecords[len(wholesaleRecords)-1][0] < retailRecords[len(retailRecords)-1][0]):
        end_date = wholesaleRecords[len(wholesaleRecords)-1][0]
    else:
        end_date = retailRecords[len(retailRecords)-1][0]
    
    arrival = smoothArray([row[0] for row in wholesaleRecords] , [row[1] for row in wholesaleRecords],end_date)
    wp = smoothArray([row[0] for row in wholesaleRecords] , [row[2] for row in wholesaleRecords],end_date)
    rp = smoothArray([row[0] for row in retailRecords] , [row[1] for row in retailRecords],end_date)
    
    # We Have got all things... Time to insert to database
    
    for i in range(0,len(arrival)):
        query = "INSERT INTO expoAvgSmoothedData(dateofdata,centreid,wholesaleprice,retailprice,arrivalsintons) VALUES ( '"+ str(arrival[i][0]) + "'," + str(centreid) + "," + str(wp[i][1]) + "," + str(rp[i][1]) + "," + str(arrival[i][1]) +" )"
        cursor.execute(query)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
    conn = psycopg2.connect(conn_string) 
    cursor = conn.cursor()

	# Get centers
    query = "select distinct centreid from centres order by centreid"
    cursor.execute(query)  
    records = cursor.fetchall()
    centres = []
    for record in records:
        centres.append(str(record[0]))
        
    # Currently this code will add data of only 4 centres
    # Mumbai, Patna, A'bad , Bengaluru
    centres = [44,50,3,7]
    for centre in centres:
        smoothPrices_Arrivals(centre)
        print centre
    