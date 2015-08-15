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
import scipy,numpy
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

@route('/method2')
def method2():    
    query = "Select state from states order by state"
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'" 
    conn = psycopg2.connect(conn_string) 
    cursor = conn.cursor()
    cursor.execute(query)  
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


@post('/diffPlot')
def graphPlot():
    center = request.forms.get('center')
    wholesalePriceC = str(request.forms.get('wholesalePriceC'))
    retailPriceC = str(request.forms.get('retailPriceC'))
    arrivalC = str(request.forms.get('arrivalC'))
    year = request.forms.get('year')
    
    query = "SELECT dateofdata, wholesaleprice, retailprice , arrivalsintons FROM MovingAvgSmoothedData m, centres c where extract(year from dateofdata) = " + year + " and m.centreid = c.centreid and c.centrename ='" + center +"' order by dateofdata"
    
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    
    dateofdata = [row[0] for row in records]
    wp = [row[1] for row in records]
    rp = [row[2] for row in records]
    arrival = [row[3] for row in records]
    
    # Plot It
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    if(wholesalePriceC == "wholesalePriceC"):
        ax.plot(dateofdata,wp, color = 'r', label='Wholesale Rate Per KG') # Red color
    if(retailPriceC == "retailPriceC"):
        ax.plot(dateofdata,rp, color = 'b', label='Retail Rate Per KG')    # Blue color
    
    if(arrivalC == "arrivalC"):
        ax2 = ax.twinx()
        ax2.plot(dateofdata,arrival,color = 'c', label = 'Arrival')
        
    fig.set_size_inches(20,12)
    plt.show()
    io = StringIO.StringIO()
    fig.savefig(io, format='png')
    data = io.getvalue().encode('base64')
    return html.format(data)
    
    
run(host='localhost', port=8080, debug=True)