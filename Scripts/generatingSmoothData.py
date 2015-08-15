# This file generates smooth data, moving average with some weights.

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


def smoothArray(dateofdata, array, end_date):
    start_date = "01/01/06"
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%y").date()
    
    # end_date = dateofdata[len(dateofdata) - 1]
    
    new_data = []
    i=0 # To keep track over the arrays passed
    while(start_date <= end_date):
        if(start_date == dateofdata[i]):
            # data for this date is present
            if(i<6):
                # Simply add to final array
                new_data.append([start_date,array[i]])                
            else:
                # Smooth
                sum = 0
                count = 0
                mul_factor = 7
                
                if(array[i] != 0 and str(array[i]) != "None"):
                    sum = sum + array[i] *mul_factor
                    count = count + mul_factor
                
                mul_factor = 1
                
                last_index = len(new_data)-1
                for j in range(last_index-5,last_index+1):
                    if(new_data[j][1] != 0):
                        sum = sum + new_data[j][1] * mul_factor
                        count = count + mul_factor
                    mul_factor = mul_factor +1
                    
                new_data.append([start_date, (sum/count)])
                
            start_date = start_date + datetime.timedelta(days=1)
            i = i+1 
        else:
            # Data for this date is missing
            if(i<6):
                new_data.append([start_date,array[i]])
            else:
                # Smooth
                sum = 0
                count = 0
                mul_factor = 6
                
                last_index = len(new_data)-1
                for j in range(last_index-5,last_index+1):
                    if(new_data[j][1] != 0):
                        sum = sum + new_data[j][1] * mul_factor
                        count = count + mul_factor
                    mul_factor = mul_factor -1
                    
                new_data.append([start_date, (sum/count)])
            
            start_date = start_date + datetime.timedelta(days=1)
    
    return new_data


def smoothPrices_Arrivals(centreid):
    
    query = "select dateofdata, sum(ArrivalsInTons), avg(ModalPriceRsQtl)/100 from wholesaleoniondata as w,mandis m where m.centreid = " + str(centreid) + " and w.mandicode = m.mandicode group by dateofdata order by dateofdata;"
    
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(query)
    wholesaleRecords = cursor.fetchall()
	
    query = "select DateOfData,Price from RetailOnionData as r where r.centreid = "+ str(centreid) +" order by DateOfData"
    cursor.execute(query)
    retailRecords = cursor.fetchall()
    
    if(wholesaleRecords[len(wholesaleRecords)-1][0] < retailRecords[len(retailRecords)-1][0]):
        end_date = wholesaleRecords[len(wholesaleRecords)-1][0]
    else:
        end_date = retailRecords[len(retailRecords)-1][0]
    
    arrival = smoothArray([row[0] for row in wholesaleRecords] , [row[1] for row in wholesaleRecords],end_date)
    wp = smoothArray([row[0] for row in wholesaleRecords] , [row[2] for row in wholesaleRecords],end_date)
    rp = smoothArray([row[0] for row in retailRecords] , [row[1] for row in retailRecords],end_date)
    
    # We Have got all things... Time to insert to database
    
    for i in range(0,len(arrival)):
        query = "INSERT INTO MovingAvgSmoothedData(dateofdata,centreid,wholesaleprice,retailprice,arrivalsintons) VALUES ( '"+ str(arrival[i][0]) + "'," + str(centreid) + "," + str(wp[i][1]) + "," + str(rp[i][1]) + "," + str(arrival[i][1]) +" )"
        cursor.execute(query)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    centres = [44]
    for centre in centres:
        smoothPrices_Arrivals(centre)
    