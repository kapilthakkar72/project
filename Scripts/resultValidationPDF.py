'''

Script To generate PDFs from the results of correlation

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
from matplotlib.backends.backend_pdf import PdfPages

'''

This function reads the corre file and returns the required result in following format
result[i][0] : centre
result[i][1] : date
result[i][2] : arrival_corr
result[i][3] : wholesale_corr

'''
def readFile(filename):
	result = []
	for line in open('corre','r').readlines():
		index = line.find("Yuppiiieee!!! FOUND ONE... :")
		if(index != -1):
			centreIndex = line.find("Centre:")
			centreIndex = centreIndex + len("Centre:")

			# Centre Starts Here
			dateIndex = line.find("date:")

			# Convert string to int, to get centre Number
			centre = int(line[centreIndex:dateIndex-1])

			# Got Centre
			dateIndex = dateIndex + len("date:") + 1
			# Date
			date = line[dateIndex:dateIndex+10]
			date = datetime.datetime.strptime(date, "%Y-%m-%d")

			dateIndex = dateIndex +22
			spaceIndex = line.find(" ",dateIndex)
			arrival_corr = float(line[dateIndex:spaceIndex])
			wholesale_corr = float(line[spaceIndex+1:len(line)-1])

			x = (centre,date,arrival_corr,wholesale_corr)
			result.append(x)

			# print str(x)	
	return result

'''

getData(centre,start_date):

This Function returns 
[0] : dateofdata
[1] : wholesaleprice
[2] : arrivalsintons

'''

def getData(centre,start_date):
	end_date = start_date + relativedelta(days=60)

	query = "select dateofdata,wholesaleprice,arrivalsintons from smoothed_data where dateofdata>='" + str(start_date) +"' and dateofdata <= '" + str(end_date) +"' and centreid = " + str(centre) + " order by dateofdata;"

	print query

	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	conn = psycopg2.connect(conn_string) 
	cursor = conn.cursor()
	cursor.execute(query)  
	records = cursor.fetchall()
	return records

def correlation(arrival1,arrival2):
    arrival1 = np.array(arrival1,dtype = float)
    arrival2 = np.array(arrival2,dtype = float)

    meanarrival1 = np.mean(arrival1)
    meanarrival2 = np.mean(arrival2)

    sx = 0.0
    sy = 0.0

    for i in range(0,len(arrival1)):
    	sx = sx + (arrival1[i] - meanarrival1) * (arrival1[i] - meanarrival1)
    	sy = sy + (arrival2[i] - meanarrival2) * (arrival2[i] - meanarrival2)
    denom = math.sqrt(sx*sy)

    floatZero = 0.0
    if str(denom) == str(floatZero):
        return (-5.0,-5.0)

    maxdelay = 15
    corr = []
    lag = []

    for delay in range(-maxdelay,maxdelay) :
    	sxy = 0.0
    	for i in range(0,len(arrival1)):
    		j = i+ delay
    		if(j<0 or j>=len(arrival2)):
    			continue
    		else:
    			sxy = sxy + (arrival1[i] - meanarrival1) * (arrival2[j] - meanarrival2)


    	r = sxy / denom
    	# print str(r)
    	corr.append(r)
    	lag.append(delay)

    min = 2
    index = -1
    for i in range(0,len(corr)):
    	if(min > corr[i]):
    		min = corr[i]
    		index = i;

    max = -2
    index2 = -1
    for i in range(0,len(corr)):
    	if(max < corr[i]):
    		max = corr[i]
    		index2 = i;

    # print "Correlation Min:" +str(min) + "  At Lag: " + str(lag[index])
    # print "Correlation Min:" +str(max) + "  At Lag: " + str(lag[index2])
    # print "Pearson Correlation:" + str(stats.pearsonr(arrival1,arrival2))

    return [max,float(lag[index])]

def wholesale_correlation(price1,price2,lagi):

    price1 = np.array(price1,dtype = float)
    price2 = np.array(price2,dtype = float)

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
    	if delay == round(lagi):
    		return r
    return -6

def createPDF(centre,date,arrival_corr,wholesale_corr):
	# print "Date"
	# print date
	thisYeardata = getData(centre,date)
	lastYearData = getData(centre, date-relativedelta(years=1))

	# print "This Year Data:"
	# print thisYeardata

	# print "Last Year Data:"
	# print lastYearData

	# Separate out Arrivals, WP, according to date

	# Extracting arrival and wp
	arrival1 = []
	arrival2 = []
	wp1 = []
	wp2 = []
	joinedDate = []

	for rec1 in thisYeardata:
		for rec2 in lastYearData:
			if(rec1[0].month == rec2[0].month and rec1[0].day == rec2[0].day):
				joinedDate.append(rec1[0])
				wp1.append(rec1[1])
				arrival1.append(rec1[2])

				wp2.append(rec2[1])
				arrival2.append(rec2[2])
	# Get the correlation and lag 
	temp = correlation(arrival1,arrival2)

	corr = temp[0]
	lag = int(math.floor(temp[1]))

	new_wp_corr = wholesale_correlation(wp1,wp2,lag)

	# Shift them According to lag
	# Second Array needs to be shifted

	if(lag > 0 ): # Shift array left
		arrival2 = arrival2[lag:]
		wp2 = wp2[lag:]
		# Append Zeros At the end
		for i in range(0,lag):
			arrival2.append(0.0)
			wp2.append(0.0)
	elif(lag < 0):	# Shift array right  
		lag = 0 - lag 
		original_size = len(arrival2)
		# Append zeros
		for i in range(0,lag):
			arrival2 = [0] + arrival2
			wp2 = [0] + wp2
		# Sublist
		arrival2 = arrival2[0:original_size]
		wp2 = wp2[0:original_size]


	# Time to plot and save it as PDF
	title = "Centre: " + str(centre) + " Date: " + str(date) + " Lag:"+str(lag) + " old arr_corr:" + str(arrival_corr) + " whole_corr:" + str(wholesale_corr) + " new: arr_corr:" + str(corr) + " whole_corr:" + str(new_wp_corr) + ".pdf"
	with PdfPages(title) as pdf:		
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		ax.plot(joinedDate,arrival1, color = 'b') 	 # Red color
		ax.plot(joinedDate,arrival2, color = 'b', linestyle= '--')    # Blue color
		# ax.legend(['Arrival This Year','Arrival Last Year'])
		ax2 = ax.twinx()
		ax2.plot(joinedDate,wp1, color = 'y')
		ax2.plot(joinedDate,wp2, color = 'y', linestyle= '--')
		# ax2.legend(['Wholesale This Year','Wholesale Last Year'])
		
		# plt.title(title)
		# pdf.savefig()  # saves the current figure into a pdf page
		fig.set_size_inches(20,12)
		plt.show()
		# plt.close()

if __name__ == "__main__":
	# Read the file
	 # fileResult = readFile("corre")

	# Process Each result of the file
	# for oneResult in fileResult:
	# 	centre = oneResult[0]
	# 	date = oneResult[1]
	# 	arrival_corr = oneResult[2]
	# 	wholesale_corr = oneResult[3]

	# 	if(arrival_corr < 0.6 or centre != 16 ):
	# 		continue;

	# 	createPDF(centre,date,arrival_corr,wholesale_corr)

	centre = 3
	date = datetime.datetime.strptime("2011-11-07", "%Y-%m-%d")
	arrival_corr = 0.698170666739
	wholesale_corr = -0.230796186701

	createPDF(centre,date,arrival_corr,wholesale_corr)


