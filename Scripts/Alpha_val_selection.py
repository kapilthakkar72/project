'''
    This file will calculate the Mean of Sum of Squared errors (MSSE),
    for each value of Alpha starting from 0.1 to 0.9, so in total
    9 values, year-wise.
    
    The Centre in consideration here will be 'Mumbai' for now, which
    can be changed later.
    
'''

import pyma
import psycopg2
import numpy
import datetime

# This function is used to clean the data and the value which is missing, previous value is replicated
def cleanDataArray(dateofdata,array,start_date,end_date):
    new_data = []
    i=0 # To keep track over the arrays passed
    while(start_date <= end_date):
        if(i<len(dateofdata) and start_date == dateofdata[i]):
            new_data.append([start_date,array[i]])
            start_date = start_date + datetime.timedelta(days=1)
            i = i+1 
        else:
            # Data for this date is missing
            if(i==0):
                new_data.append([start_date,0])
            else:
                new_data.append([start_date,new_data[len(new_data)-1][1]])            
            start_date = start_date + datetime.timedelta(days=1)    
    return new_data

# This function will return the data for the given year and centreid
# Format ::: [[dateofdata,arrival,wp,rp],[...],...]
# Note that this function will also try to fill the voids i.e. if any data is missing for anydate
# with the replication policy. That is value of previous day will be replicated
def getDataForYear(centreid,year):
    result = []
    
    # First fetching the wholesale data
    query = "select dateofdata, coalesce(sum(ArrivalsInTons),0), coalesce(avg(ModalPriceRsQtl)/100,0) from wholesaleoniondata as w,mandis m where m.centreid = " + str(centreid) + " and w.mandicode = m.mandicode and extract(year from dateofdata) = " + str(year) + " group by dateofdata order by dateofdata;"
    
    conn_string = "host='localhost' dbname='onion' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(query)
    wholesaleRecords = cursor.fetchall()
	
    # Now fetching the retail data
    query = "select DateOfData,coalesce(Price,0) from RetailOnionData as r where r.centreid = "+ str(centreid) +" and extract(year from dateofdata) = " + str(year) + "  order by DateOfData"
    cursor.execute(query)
    retailRecords = cursor.fetchall()
    
    # Time to clean them, by replicating if data for a date does not exist
    strYear = ""
    if(year%100 < 10):
        strYear = "0" + str(year%100)
    else:
        strYear = str(year%100)
        
    start_date = "01/01/" + str(strYear)
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%y").date()
    
    end_date = "12/31/" + str(strYear)
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%y").date()
    
    # Time to clean the data
    arrivalCleaned = cleanDataArray([row[0] for row in wholesaleRecords],[row[1] for row in wholesaleRecords],start_date,end_date)
    wpCleaned = cleanDataArray([row[0] for row in wholesaleRecords],[row[2] for row in wholesaleRecords],start_date,end_date)
    rpCleaned = cleanDataArray([row[0] for row in retailRecords],[row[1] for row in retailRecords],start_date,end_date)
    
    # Combine them to form a single 2D array of the format required
    for i in range(0,len(arrivalCleaned)):
        result.append([arrivalCleaned[i][0],arrivalCleaned[i][1], wpCleaned[i][1], rpCleaned[i][1]])
    
    return result
    
# This function returns the MSSE for the given alpha value and array
def getMSSE(array, alpha):
    array = numpy.array(array)
    #print array
    array = ["%.2f" % a for a in array]
    
    smoothedArray = []
    
    # Creating EMA Object
    EMA = pyma.EMA(alpha)
    
    # Getting EMA (Exponential moving avg) of the given array with given alpha
    for val in array:
        smoothedArray.append(EMA.compute(val))
    
    temp = []
    for s in smoothedArray:
        temp.append(float(s))
    
    smoothedArray = temp
    
    temp = []
    for a in array:
        temp.append(float(a))
    array = temp
    # smoothedArray = smoothedArray.asType(float)    
    # Time to calculate SSE
    SSE = 0
    
    for i in range(0,len(array)):
        SSE = SSE + (array[i] - smoothedArray[i]) * (array[i] - smoothedArray[i])
        
    return SSE / (len(array));

# Main Function to drive program
if __name__ == "__main__":
    # 44 is the centreid for Mumbai
    centre = 44
    year = 2006
    end_year = 2014
    while(year <= end_year):
        # This function will return the data for the given year and centreid
        # Format ::: [[dateofdata,arrival,wp,rp],[...],...]
        # Note that this function will also try to fill the voids i.e. if any data is missing for anydate
        # with the replication policy. That is value of previous day will be replicated
        yeardata = getDataForYear(centre,year)
        
        # This year data :
        #print yeardata
        
        alpha = 0.1
        delta = 0.1
        while(alpha < 1):
            # Its time to get the MSSE Value for each parameter
            
            # print [row[1] for row in yeardata]
            
            arrivalMSSE = getMSSE([row[1] for row in yeardata],alpha)
            wpMSSE = getMSSE([row[2] for row in yeardata],alpha)
            retailMSSE = getMSSE([row[3] for row in yeardata],alpha)
            
            # Time to print these value properly
            print "YEAR:," + str(year) + " ,alpha:," + str(alpha) + " ,arrivalMSSE:," + str(arrivalMSSE) + ", wpMSSE:," + str(wpMSSE) + " ,retailMSSE:," + str(retailMSSE)
            
            alpha = alpha + delta
            
        # Go to next Year
        year = year + 1
        