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
# import pywt


html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}"  height="800" width="1100"/>
    </body>
</html>
'''

@route('/')
def index():
	return template('index')


@get('/method3')
def method3():
	query = "Select state from states order by state"
	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (conn_string) 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string) 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	#print "Connected!\n"
	# execute our Query
	cursor.execute(query)  
	# retrieve the records from the database
	records = cursor.fetchall()
	sts = []
	for record in records:
		sts.append(record[0])

	# Get years
	query = "select distinct extract(year from DateOfData) from WholeSaleOnionData order by extract(year from DateOfData)"
	cursor.execute(query)  
	records = cursor.fetchall()
	yrs = []
	for record in records:
		yrs.append(int(record[0]))

	# Get centers
	query = "select distinct CentreName,centreid from centres order by CentreName"
	cursor.execute(query)  
	records = cursor.fetchall()
	cts = []
	ids = []
	for record in records:
		cts.append(str(record[0]))
		ids.append(str(record[1]))


	conn.close()
	return template('method3Menu', states=sts, years=yrs, centers = cts, centreids = ids)


@get('/method1')
def method1():
	# Menu for cluster formation goes here...
	query = "Select state from states"
	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (conn_string) 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string) 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	#print "Connected!\n"
	# execute our Query
	cursor.execute(query)  
	# retrieve the records from the database
	records = cursor.fetchall()
	sts = []
	for record in records:
		sts.append(record[0])

	# Get years
	query = "select distinct extract(year from DateOfData) from WholeSaleOnionData"
	cursor.execute(query)  
	records = cursor.fetchall()
	yrs = []
	for record in records:
		yrs.append(int(record[0]))

	conn.close()
	return template('method1Menu', states=sts, years=yrs)


@route('/method2')
def method2():
	'''
	Here I need to get the retail and wholesale Price... and compare their difference
	But before that to get the input I need to give/provide user options to select the center/State
	So this will just return the GUI ... 
	But this can be copied from the method 1
	Jay Yogeshwar!
	'''
	query = "Select state from states order by state"
	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (conn_string) 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string) 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	#print "Connected!\n"
	# execute our Query
	cursor.execute(query)  
	# retrieve the records from the database
	records = cursor.fetchall()
	sts = []
	for record in records:
		sts.append(record[0])

	# Get years
	query = "select distinct extract(year from DateOfData) from WholeSaleOnionData order by extract(year from DateOfData)"
	cursor.execute(query)  
	records = cursor.fetchall()
	yrs = []
	for record in records:
		yrs.append(int(record[0]))

	# Get centers
	query = "select distinct CentreName from centres order by CentreName"
	cursor.execute(query)  
	records = cursor.fetchall()
	cts = []
	for record in records:
		cts.append(str(record[0]))


	conn.close()
	return template('method2Menu', states=sts, years=yrs, centers = cts)



@post('/cluster')
def formCluster():
	# Get data from the form
	state = request.forms.get('state')
	year = request.forms.get('year')
	month = request.forms.get('month')

	# Date, State, Mandi, Arrival, Modal Price

	query = ""
	# Now we need to fetch data and form clusters
	if(state == "0"):
		# All States
		if(month == "0"):
			# All Months
			query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s where w.StateCode = s.StateCode and extract(year from dateofdata)=" + year + " order by dateofdata"
		else:
			#Particular Month
			query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s where w.StateCode = s.StateCode and extract(year from dateofdata)=" + year + " and extract(month from dateofdata)="+month+" order by dateofdata"
	else:
		# Particular state
		if(month == "0"):
			# All Months
			query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s where w.StateCode = s.StateCode and State='"+ state+"' and extract(year from dateofdata)=" + year + " order by dateofdata"
		else:
			#Particular Month
			query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s where w.StateCode = s.StateCode and State='"+ state+"' and extract(year from dateofdata)=" + year + " and extract(month from dateofdata)="+month+" order by dateofdata"


	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (conn_string) 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string) 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	#print "Connected!\n"
	# execute our Query
	cursor.execute(query)  
	# retrieve the records from the database
	records = cursor.fetchall()
	
	justModalPrices = []
	algoData = []

	for record in records:
	#print 'Printed outside' + str(record[0])
		if(isinstance(record[4],decimal.Decimal)):
			#print 'Printed inside' + str(record[0])
			justModalPrices.append(record[4])
			x=[]
			x.append(record[4])
			algoData.append(x)

	conn.close()

	if(algoData != []):
		# Form Clusters

		k_means = cluster.KMeans(n_clusters=2,max_iter=300, n_init=10)
		k_means.fit(algoData)

		print "Cluster Centers:" + str(k_means.cluster_centers_)

		dataWithCluster = zip(k_means.labels_, records)
		justModalPricesWithCluster = zip(k_means.labels_,justModalPrices)

		cluster1 = []
		cluster2 = []

		# print dataWithCluster

		centroids=[]
		centroids2DArray = k_means.cluster_centers_

		centroids.append(centroids2DArray[0][0])
		centroids.append(centroids2DArray[1][0])

		for point in justModalPricesWithCluster:
			if(int(point[0]) == 0):
				cluster1.append(point[1])
			else:
				cluster2.append(point[1])

		
		plt.plot(cluster1, len(cluster1) * [1], "x",color='g')
		plt.plot(cluster2, len(cluster2) * [1], "x",color='b')
		plt.plot(centroids , len(centroids) * [1] , "o",color='r')
		#plt.show()
		#plt.savefig(StringIO.StringIO())
		'''
		img = StringIO.StringIO()
		plt.savefig(img)
		img.seek(0)
		return send_file(img, mimetype='image/png')
		
		'''
		fig = plt.figure()

		ax = fig.add_subplot(1,1,1)
		ax.plot(cluster1, len(cluster1) * [1], "x",color='g')
		ax.plot(cluster2, len(cluster2) * [1], "x",color='b')
		ax.plot(centroids , len(centroids) * [1] , "o",color='r')

		#canvas = FigureCanvas(fig)
		#png_output = StringIO.StringIO()
		#canvas.print_png(png_output)
		#response.content_type = 'image/png'
		#return (png_output.getvalue() + "<br>Kapil Thakkar")
		io = StringIO.StringIO()
		fig.savefig(io, format='png')
		data = io.getvalue().encode('base64')
		return html.format(data)

		return "KT"

	else:
		return "Data Not Present"

@post('/diffPlot')
def formCluster():
	# Get data from the form
	state = request.forms.get('state')
	print "State: " + state
	year = request.forms.get('year')
	print "Year: " + year
	month = request.forms.get('month')
	center = request.forms.get('center')
	variation = int(request.forms.get('variation'))
	option = request.forms.get('opt')
	wholesalePriceC = str(request.forms.get('wholesalePriceC'))
	# print wholesalePriceC
	retailPriceC = str(request.forms.get('retailPriceC'))
	# print retailPriceC
	absoluteDiffC = str(request.forms.get('absoluteDiffC'))
	# print absoluteDiffC
	relativeDiffC = str(request.forms.get('relativeDiffC'))
	# print relativeDiffC
	arrivalC = str(request.forms.get('arrivalC'))
	# print arrivalC
	retailDiff = str(request.forms.get('retailDiff'))
	# print retailDiff
	rmwAnalysis = str(request.forms.get('rmwAnalysis'))
	# print rmwAnalysis


	# This query fetches the wholesale data... queryRetail will do the work for retail data
	
	# Wholesale : Date, State, Mandi, Arrival, Modal Price

	query = ""
	queryRetail = ""
	# Now we need to fetch data and form clusters
	if(option == "statewise"):
		if(state == "0"):
			# All States
			if(month == "0" and year != "0"):
				# All Months
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s, mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and extract(year from dateofdata)=" + year + " order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s, centres as c where c.StateCode = s.StateCode and r.centreid = c.centreid and extract(year from DateOfData) =" + year + " order by DateOfData"

			if(month == "0" and year == "0"):
				# All Months
				query = query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s, mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s, centres as c where c.StateCode = s.StateCode and r.centreid = c.centreid order by DateOfData"
			
			if(month != "0" and year != "0"):
				#Particular Month
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s, mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and extract(year from dateofdata)=" + year + " and extract(month from dateofdata)="+month+" order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s , centres as c where r.centreid = c.centreid and c.StateCode = s.StateCode and extract(year from DateOfData)=" + year + " and extract(month from dateofdata)="+month+" order by dateofdata"

			if(month != "0" and year == "0"):
				#Particular Month
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s, mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and extract(month from dateofdata)="+month+" order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s  , centres as c where r.centreid = c.centreid and c.StateCode = s.StateCode and extract(month from dateofdata)="+month+" order by dateofdata"
		else:
			# Particular state
			if(month == "0" and year != "0"):
				# All Months
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s, mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and State='"+ state+"' and extract(year from dateofdata)=" + year + " order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, STATES as s  , centres as c where r.centreid = c.centreid and c.StateCode = s.StateCode and extract(year from dateofdata)=" + year + " and state = '" + state + "' order by DateOfData"

			if(month == "0" and year == "0"):
				# All Months
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s , mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and State='"+ state+"' order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, STATES as s  , centres as c where r.centreid = c.centreid and c.StateCode = s.StateCode and state = '" + state + "' order by DateOfData"

			if(month != "0" and year != "0"):
				#Particular Month
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s , mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and State='"+ state+"' and extract(year from dateofdata)=" + year + " and extract(month from dateofdata)="+month+" order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, STATES as s  , centres as c where r.centreid = c.centreid and c.StateCode = s.StateCode and extract(year from dateofdata)=" + year + " and state = '" + state + "' and extract(month from DateOfData) = " + month + " order by DateOfData"

			if(month != "0" and year == "0"):
				#Particular Month
				query = "select DateOfData, State, MandiName, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w, STATES as s , mandis m where w.mandicode=m.mandicode and m.StateCode = s.StateCode and State='"+ state+"' and extract(month from dateofdata)="+month+" order by dateofdata"
				queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, STATES as s  , centres as c where r.centreid = c.centreid and c.StateCode = s.StateCode and state = '" + state + "' and extract(month from DateOfData) = " + month + " order by DateOfData"
	else: # option = "centerwise"
			# Particular center
		if(month == "0" and year != "0"):
			# All Months
			query = "select dateofdata,state, mandiname, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w,mandis m, states as s,  centres c where m.centreid = c.centreid and c.centreName = '" + center + "' and w.mandicode = m.mandicode and s.StateCode = c.StateCode and extract(year from dateofdata)=" + year + " order by dateofdata";
			queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s , centres as c  where r.centreid = c.centreid and s.StateCode = c.StateCode and extract(year from dateofdata)=" + year + " and CentreName = '" + center + "' order by DateOfData"

		if(month == "0" and year == "0"):
			# All Months
			query = "select dateofdata,state,mandiname, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w,mandis m, states as s,  centres c where m.centreid = c.centreid and c.centreName = '" + center + "' and w.mandicode = m.mandicode and s.StateCode = c.StateCode order by dateofdata";
			queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s , centres as c  where r.centreid = c.centreid and s.StateCode = c.StateCode and CentreName = '" + center + "' order by DateOfData"

		if(month != "0" and year != "0"):
			#Particular Month
			query = "select dateofdata,state,mandiname, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w,mandis m, states as s,  centres c where m.centreid = c.centreid and c.centreName = '" + center + "' and w.mandicode = m.mandicode and s.StateCode = c.StateCode and extract(month from dateofdata)="+month+" and extract(year from dateofdata)=" + year + " order by dateofdata";
			
			queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s , centres as c  where r.centreid = c.centreid and s.StateCode = c.StateCode and extract(year from dateofdata)=" + year + " and CentreName = '" + center + "' and extract(month from DateOfData) = " + month + " order by DateOfData"

		if(month != "0" and year == "0"):
			#Particular Month
			query = "select dateofdata,state,mandiname, ArrivalsInTons, ModalPriceRsQtl from wholesaleoniondata as w,mandis m, states as s,  centres c where m.centreid = c.centreid and c.centreName = '" + center + "' and w.mandicode = m.mandicode and s.StateCode = c.StateCode and extract(month from dateofdata)="+month+"  order by dateofdata";
			queryRetail = "select DateOfData,state,CentreName,Longitude,latitude,Price from RetailOnionData as r, states as s , centres as c  where r.centreid = c.centreid and s.StateCode = c.StateCode and CentreName = '" + center + "' and extract(month from DateOfData) = " + month + " order by DateOfData"



	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (conn_string) 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string) 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	#print "Connected!\n"
	# execute our Query
	cursor.execute(query)  
	# retrieve the records from the database
	wholesaleRecords = cursor.fetchall()

	cursor.execute(queryRetail)
	retailRecords = cursor.fetchall()

	print "Retail Query"
	print queryRetail
	print "Wholesale Query"
	print query

	conn.close()
	
	dateListW=[]
	priceW = []
	dateListR=[]
	priceR = []
	arrival = []

	# for record in wholesaleRecords:
	# 	if(isinstance(record[4],decimal.Decimal)):
	# 		justModalPrices.append(record[4])
	# 		justWholesaleDates.append(record[0])

	# for record in retailRecords:
	# 	if(isinstance(record[5],decimal.Decimal)):
	# 		justRetailPrices.append(record[5])
	# 		justRetailDates.append(record[0])

	date = ""
	price = 0.0
	count = 0
	tempArrival = decimal.Decimal(0.0)
	for record in wholesaleRecords:
		if(date == record[0] and isinstance(record[4],decimal.Decimal)):
			price = price + record[4]
			count = count+1
			if(isinstance(record[3],decimal.Decimal)):		# For arrival
				tempArrival = tempArrival + record[3]
 		else:
			if(price != 0):
				dateListW.append(date)
				priceW.append((price/count)/100) 	# To get the per KG price from per Quintal Price
				arrival.append(tempArrival)
				if(isinstance(record[4],decimal.Decimal)):
					date = record[0]
					price = record[4]
					count = 1
					if(isinstance(record[3],decimal.Decimal)):		# For arrival
						tempArrival = record[3]
			else:
				if(isinstance(record[4],decimal.Decimal)):
					date = record[0]
					price = record[4]
					count = 1
					if(isinstance(record[3],decimal.Decimal)):		# For arrival
						tempArrival = record[3]

	# if Last record left out
	if(len(dateListW)!=0):
		if(date != dateListW[len(dateListW)-1]):
			dateListW.append(date)
			priceW.append(price/(count*100))
			arrival.append(tempArrival)


	date = ""
	price = 0.0
	count = 0
	for record in retailRecords:
		if(isinstance(record[5],decimal.Decimal)):
			if(record[5] == decimal.Decimal(0)):
				continue;
		if(date == record[0] and isinstance(record[5],decimal.Decimal)):
			price = price + record[5]
			count = count+1
		else:
			if(price != 0):
				dateListR.append(date)
				priceR.append(price/count)
				if(isinstance(record[5],decimal.Decimal)):
					date = record[0]
					price = record[5]
					count = 1
			else:
				if(isinstance(record[5],decimal.Decimal)):
					date = record[0]
					price = record[5]
					count = 1

	
	# if Last record left out
	if(len(dateListR)!=0):
		if(date != dateListR[len(dateListR)-1]):
			dateListR.append(date)
			priceR.append(price/count)

	
	'''
	-----------------------------------------------------------------------------------
	|	This code is just to print the fetched data.... Used for testing... 		  |
	-----------------------------------------------------------------------------------

	print "Retail Data"
	i=0
	for retail in dateListR:
		print str(retail) + "," + str(priceR[i])
	i+=1

	print "wholesale Data"
	i=0
	for wholesale in dateListW:
		print str(wholesale) + "," + str(priceW[i])
		i+=1
	
	------------------------------------------------------------------------------------
	|																				   |  
	------------------------------------------------------------------------------------
	'''

	# Code to get the difference between wholesale and retail price

	# Now I have to perform join operation on Date attribute... For that what i know is only nested loop join...
	# So will perform that...
	dateJoined = []
	diffJoined = []
	percJoined = []

	retailPriceJoined = []
	wholesalePriceJoined = []
	i=0 	# Will be used to access the retail price from date
	for retail in dateListR:
		j=0		# Will be used to access the wholesale price from date
		for wholesale in dateListW:
			if(retail == wholesale):
				# print str(retail) + "matched"
				# print str(i) + " " + str(j)
				# print str(priceR[i]) + " " + str(priceW[j])
				# print str(priceR[i]-priceW[j])
				dateJoined.append(retail)
				retailPriceJoined.append(priceR[i])
				wholesalePriceJoined.append(priceW[j])
				diffJoined.append(priceR[i]-priceW[j])
				percJoined.append((priceR[i]-priceW[j]) * 100 / priceW[j])
				break
			j=j+1
		i=i+1

	
	
		'''
	# Code for printing the arrival values

	print "Arrivals...\n"

	i=1
	for a in arrival:
		print str(i) + "  " + str(a)
		i=i+1
		'''

	
	#######################################################################################
	# 			Code to smooth out the arrival, it will be average over 5 days 			  #
	#######################################################################################
	daysToSmooth = 5
	temp = 0
	smoothedArrival = []
	arrivalDate = []
	total = 0
	i = 0 # To keep track of date
	smoothedArrival.append(arrival[0])
	arrivalDate.append(dateListW[0])
	for a in arrival:
		total = total + a
		temp = temp +1
		i = i+1
		if(temp == 5):
			smoothedArrival.append(total)
			arrivalDate.append(dateListW[i-1])
			total = 0
			temp = 0

	if(temp != 0): 
		# Date is not multiple of 5
		smoothedArrival.append(total)
		arrivalDate.append(dateListW[i-1])

	#########################################################################################

	#########################################################################################
	#							FOURIER AND WAVELET TRANSFORM								#
	#########################################################################################
	# if(len(priceW) != 0):
	# 	fourier = np.fft.rfft(priceW)
	# 	freq = np.fft.fftfreq(len(fourier), 1)
	# 	plt.figure()
	# 	plt.plot( freq, np.abs(fourier) )
	# 	plt.figure()
	# else:
	# 	print "Can not find FFT of 0 length array"

	
	# wavelet = pywt.dwt(priceW, 'db1')

	# print "Fourier Series"
	# print fourier
	# print "Wavelet Transform"
	# print wavelet

	# Plot the fourier tranform
	
	# plt.plot(freq, np.angle(fourier) )
	# plt.show()
	#########################################################################################
	#						END OF FOURIER AND WAVELET TRANSFORM 							#
	#########################################################################################


	#########################################################################################
	#							HISTOGRAM OF PRICE DITRIBUTION 								#
	#########################################################################################

	priceWFloat = np.array(priceW,dtype = float)
	priceRFloat = np.array(priceR,dtype = float)
	arrivalFloat = np.array(arrival,dtype = float)

	# Lets wholesale prices... 
	mu = np.average(priceWFloat)

	temp = 0
	for price in priceWFloat:
		temp = temp + (price-mu)*(price-mu)
	temp = temp / len(priceWFloat)
	sd = math.sqrt(temp)

	newPriceW = []
	for price in priceWFloat:
		newPriceW.append((price-mu)/sd)

	# print "Min: "+ str(min(priceWFloat))
	# print "Max: "+ str(max(priceWFloat))
	# plt.hist(priceWFloat,bins=15)
	# plt.hist(np.power(priceRFloat,0.5))
	# plt.hist(np.power(arrivalFloat,0.1),bins=15)
	# plt.hist(arrivalFloat)
	# print "Min: "+ str(min(newPriceW))
	# print "Max: "+ str(max(newPriceW))
	# plt.hist(np.power(priceWFloat,0.05))
	# plt.show()

	#########################################################################################
	#						END OF	HISTOGRAM												#
	#########################################################################################


	#########################################################################################
	#						Retail Diff array 												#
	#########################################################################################

	retailDiffDate = []
	retailDiffPerc = []

	for i in range(variation,len(priceR)):
		currentPrice = priceR[i]
		prevIndex = i-variation
		previousPrice = priceR[prevIndex]
		currentDate = dateListR[i]
		perc = (currentPrice - previousPrice) / previousPrice * 100 ;
		retailDiffDate.append(currentDate)
		retailDiffPerc.append(perc)

	'''

	# Printing Array with dates
	# Only those entries which has diff greater than 100%
	for i in range(0,len(retailDiffDate)):
		if(retailDiffPerc[i] >= 100):
			print str(retailDiffDate[i]) + " : " + str(retailDiffPerc[i])

	'''

	#########################################################################################
	#						END OF RETAIL DIFF ARRAY 										#
	#########################################################################################


	#########################################################################################
	#				CODE TO PLOT THE DITRIBUTION OF RETAIL MINUS WHOLESALE 					#
	#########################################################################################


	if(rmwAnalysis == "rmwAnalysis"):
		
		# Note that we have the difference data in the following 2 arrays
		# 1. diffJoined : Contains The Absolute Difference
		# 2. dateJoined : Contains The Date on which Join is Performed

		# The thing we need to do is plot CDF/PDF(Histogram)

		# Drawing PDF
		diffJoinedFloat = np.array(percJoined,dtype = float)
		n=50	# No. of bins
		# p, x = np.histogram(diffJoinedFloat, bins=n) # bin it into n = N/10 bins
		# x = x[:-1] + (x[1] - x[0])/2   # convert bin edges to centers
		# f = UnivariateSpline(x, p, s=n)
		# plt.plot(x, f(x))
		plt.hist(diffJoinedFloat)
		plt.show()



	########################################################################################
	#			END OF CODE TO PLOT THE DITRIBUTION OF RETAIL MINUS WHOLESALE 			   #
	########################################################################################



	# plt.plot(retailPriceJoined,wholesalePriceJoined)
	# plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	if(wholesalePriceC == "wholesalePriceC"):
		ax.plot(dateListW,priceW, color = 'r', label='Wholesale Rate Per KG') # Red color
	if(retailPriceC == "retailPriceC"):
		ax.plot(dateListR,priceR, color = 'b', label='Retail Rate Per KG')    # Blue color
	if(absoluteDiffC == "absoluteDiffC"):
		ax.plot(dateJoined,diffJoined, color = 'y', label='Absolute Difference (retail - wholesale)') # Yellow Color
	if(relativeDiffC == "relativeDiffC"):
		ax.plot(dateJoined,percJoined,color = 'k' , label='Difference with respect to Wholesale Price')  # K - Black color
	if(retailDiff == "retailDiff"):
		ax.plot(retailDiffDate,retailDiffPerc,color = 'orange' , label='Difference in retail price')
	# ax.legend(['Wholesale Rate Per KG','Retail Rate Per KG','Absolute Difference (retail - wholesale)','Difference with respect to Wholesale Price','Difference in retail price'])

	ax.legend(['Retail Rate Per KG','Difference in retail price'])

	# second axis to plot the arrival

	if(arrivalC == "arrivalC"):
		ax2 = ax.twinx()
		if(month == "0"):
			ax2.plot(arrivalDate,smoothedArrival,color = 'c', label = 'Arrival')
		else:
			# ax2.plot(dateListW,arrival,color = 'c', label = 'Arrival')
			ax2.plot(arrivalDate,smoothedArrival,color = 'c', label = 'Arrival')
		# ax2.legend(['Arrival'])

	fig.set_size_inches(20,12)

	# plt.show()
	io = StringIO.StringIO()
	fig.savefig(io, format='png')
	data = io.getvalue().encode('base64')
	return html.format(data)


@post('/plotHisto')
def plotHisto():
	year = request.forms.get('year')
	print "Year: " + year
	centerID = request.forms.get('center')
	month = request.forms.get('month')


	if(month == "0"):
		query = "select ((rp-wp/100)/(wp/100))*100 from (select r.dateofdata,r.price as rp,avg(modalpricersqtl) as wp,sum(arrivalsintons) as arrival from wholesaleoniondata w,retailoniondata r,mandis m, centres c where extract(year from w.dateofdata)= " + year + " and m.centreid = "+ centerID + " and extract(year from r.dateofdata)= " + year + " and m.mandicode=w.mandicode and m.centreid=r.centreid and r.price > 0 and r.dateofdata=w.dateofdata group by r.dateofdata,r.price order by r.dateofdata desc,r.price) as k";
	else:
		query = "select ((rp-wp/100)/(wp/100))*100 from (select r.dateofdata,r.price as rp,avg(modalpricersqtl) as wp,sum(arrivalsintons) as arrival from wholesaleoniondata w,retailoniondata r,mandis m, centres c where extract(year from w.dateofdata)= " + year + " and extract(month from w.dateofdata)= " + month + " and m.centreid = "+ centerID + " and extract(year from r.dateofdata)= " + year + " and extract(month from r.dateofdata)= " + month + " and m.mandicode=w.mandicode and m.centreid=r.centreid and r.price > 0 and r.dateofdata=w.dateofdata group by r.dateofdata,r.price order by r.dateofdata desc,r.price) as k";

	'''

	select * from (select dateofdata,((rp-wp/100)/(wp/100))*100 as diff from (select r.dateofdata,r.price as rp,avg(modalpricersqtl) as wp,sum(arrivalsintons) as arrival from wholesaleoniondata w,retailoniondata r,mandis m, centres c where extract(year from w.dateofdata)= 2015 and m.centreid = 16 and extract(year from r.dateofdata)= 2015 and m.mandicode=w.mandicode and m.centreid=r.centreid and r.price > 0 and r.dateofdata=w.dateofdata group by r.dateofdata,r.price order by r.dateofdata desc,r.price) as k) as p where diff > 131 order by DateOfData ;

	'''

	# query = "select (rp-wp/100) from (select r.dateofdata,r.price as rp,avg(modalpricersqtl) as wp,sum(arrivalsintons) as arrival from wholesaleoniondata w,retailoniondata r,mandis m, centres c where extract(year from w.dateofdata)= " + year + " and m.centreid = "+ centerID + " and extract(year from r.dateofdata)= " + year + " and m.mandicode=w.mandicode and m.centreid=r.centreid and r.price > 0 and r.dateofdata=w.dateofdata group by r.dateofdata,r.price order by r.dateofdata desc,r.price) as k";

	print query

	#Define our connection string
	conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (conn_string) 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string) 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	#print "Connected!\n"
	# execute our Query
	cursor.execute(query)  
	# retrieve the records from the database
	records = cursor.fetchall()

	result = []

	for record in records:
		result.append(record[0])

	resultFloat = np.array(result,dtype = float)

	# Mean OF the Array
	print "Year: " + year
	print "Mean: " + str(np.mean(resultFloat))
	print "Standard Deviation: " + str(np.std(resultFloat))

	#################################################################################
	# 						Code to get the Correlation... 							#
	#################################################################################

	query = "select r.dateofdata,r.price as rp,avg(modalpricersqtl) as wp,sum(arrivalsintons) as arrival from wholesaleoniondata w,retailoniondata r,mandis m, centres c where extract(year from w.dateofdata)= " + year + " and m.centreid = "+ centerID + " and extract(year from r.dateofdata)= " + year + " and m.mandicode=w.mandicode and m.centreid=r.centreid and r.price > 0 and r.dateofdata=w.dateofdata group by r.dateofdata,r.price order by r.dateofdata ,r.price"
	cursor.execute(query)  
	recs = cursor.fetchall()

	print query

	# recs[i][0] : Date
	# recs[i][1] : Retail Price
	# recs[i][2] : Modal Price : Wholesale
	# recs[i][3] : Arrival

	prices = []
	arrivals = []

	for rec in recs:
		prices.append(rec[2])
		arrivals.append(rec[3])

	prices = np.array(prices,dtype = float)
	arrivals = np.array(arrivals,dtype = float)

	# We need to smooth these values before going forwards

	SMOOTHING_FACTOR = 7

	smoothedArrival = []
	smoothedPrices = []

	i = 0
	while i < len(prices):
		sumP = 0
		sumA = 0
		count = 0
		while(i < len(prices) and count<SMOOTHING_FACTOR):
			if(math.isnan(prices[i]) or math.isnan(arrivals[i])):
				i = i+1
				continue
			sumA = sumA + arrivals[i]
			sumP = sumP + prices[i]
			i = i+1
			count = count +1
		smoothedArrival.append(sumA / count)
		smoothedPrices.append(sumP / count)
		pass

	prices = smoothedPrices
	arrivals = smoothedArrival

	meanPrice = np.mean(prices)
	meanArrival = np.mean(arrivals)

	sx = 0.0
	sy = 0.0

	for i in range(0,len(prices)):
		if(math.isnan(prices[i]) or math.isnan(arrivals[i])):
			continue
		sx = sx + (prices[i] - meanPrice) * (prices[i] - meanPrice)
		sy = sy + (arrivals[i] - meanArrival) * (arrivals[i] - meanArrival)

	print "sx:" + str(sx) + " sy:"+str(sy)

	denom = math.sqrt(sx*sy)

	maxdelay = 15

	corr = []
	lag = []

	# print "denom:" + str(denom)

	for delay in range(-maxdelay,maxdelay) :
		sxy = 0.0
		for i in range(0,len(prices)):
			j = i+ delay
			if(j<0 or j>=len(prices)):
				continue
			else:
				sxy = sxy + (prices[i] - meanPrice) * (arrivals[j] - meanArrival)

		r = sxy / denom
		# print str(delay) + " : " + str(r)
		print str(r)
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

	print "Correlation Min:" +str(min) + "  At Lag: " + str(lag[index])
	print "Correlation Min:" +str(max) + "  At Lag: " + str(lag[index2])
	print "Pearson Correlation:" + str(stats.pearsonr(prices,arrivals))

	'''
	# manual calculation
	sum_price = 0;
	for p in prices:
		sum_price = p + sum_price
	price_avg = sum_price / len(prices)

	sum_arrival = 0;
	for a in arrivals:
		sum_arrival = a + sum_arrival
	arrival_avg = sum_arrival / len(arrivals)



	numerator = 0
	denom1 = 0
	denom2 = 0
	for i in range(0,len(prices)):
		numerator = numerator + (prices[i] - price_avg) * (arrivals[i] - arrival_avg)
		denom1 = denom1 + math.pow((prices[i] - price_avg),2)
		denom2 = denom2 + math.pow((arrivals[i] - arrival_avg),2)

	print "Normal: " + str( numerator / math.sqrt(denom1 * denom2) )

	print str(meanPrice) + " >>>>>>> " + str(price_avg)
	print str(meanArrival) + " >>>>>>> " + str(arrival_avg)
	print str(denom) + " >>>>>>>>>> "  + str(math.sqrt(denom1 * denom2))
	'''
	#################################################################################
	# 				END OF Code to get the Correlation... 							#
	#################################################################################

	for r in resultFloat:
		print str(r) + ","

	plt.hist(resultFloat, bins = 20 )
	# plt.show()
	conn.close()
	####### END OF PLOT HISTO METHOD ###########################	 

run(host='localhost', port=8080, debug=True)
