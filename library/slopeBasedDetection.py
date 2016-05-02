import numpy
from Utility import MADThreshold 
from Utility import smoothArray
import numpy as np
'''
This function takes 6 arguments:

1. series1 : Array of elements (int, real vals)
2. next_val_to_consider: Which Val to consider to calculate slope? Usually next Val, but for our data we take 7 days
3. smoothed: Array is smoothed or not? (True/False) If not smoothing will be done
4. default_threshold: whether to consider default threshold or not (True/False)
5. threshold: This is threshold value to consider if not default one.
6. what_to_consider :
    1. Only positive slopes
    0. Both type of slopes
    -1. Only negative slopes


returns array of tuples as follows:
(first,second,slope_value)
where first and second specifies the points between which slope was calculated. slope_value is the value of slope between those 2 points.

'''
def slopeBasedDetection(series1,smoothed1,series2,smoothed2,next_val_to_consider = 7, default_threshold = True, threshold = 0, what_to_consider = 1):
    if(smoothed1 == False):
        series1 = smoothArray(series1)
    if(smoothed2 == False):
        series2 = smoothArray(series2)
    
    n = len(series1)
    positive_slopes = []
    anomalous_pts = []
    negative_slopes = []
    i = 0
    while(i<(n-next_val_to_consider+1)):
    #for i in range(0,n-next_val_to_consider+1):
        if((series2[i+next_val_to_consider-1] - series2[i]) == 0):
            i= i+ next_val_to_consider -1
            continue
        diff = ((series1[i+next_val_to_consider-1] - series1[i]) * series2[i] )/ ((series2[i+next_val_to_consider-1] - series2[i]) * series1[i])
        if(diff < 0):
            negative_slopes.append((i,i+next_val_to_consider-1,diff))
        else:
            positive_slopes.append((i,i+next_val_to_consider-1,diff))
        i= i+ next_val_to_consider -1
    
             
    if(default_threshold == True):
        temp = []
        for x in positive_slopes:
            temp.append(x[2])
        if(len(temp)>0):
            (_,positive_threshold) = MADThreshold(temp)
        # print "Positive Threshold Value:" + str(positive_threshold)
        
    if(default_threshold == True):
        temp = []
        for x in negative_slopes:
            temp.append(x[2])
        if(len(temp)>0):
            (negative_threshold,_) = MADThreshold(temp)
        # print "Negative Threshold Value:" + str(negative_threshold)
        
    for i in range(0,len(positive_slopes)):
        if(positive_slopes[i][2] > positive_threshold):
            anomalous_pts.append(positive_slopes[i])
            
    for i in range(0,len(negative_slopes)):
        if(negative_slopes[i][2] < negative_threshold):
            anomalous_pts.append(negative_slopes[i])
    
    # Sort array according to start of window
    sorted(anomalous_pts, key=lambda x: x[0])
    
    '''
    if(what_to_consider == 1):
        for i in range(0,n):
            if(diff>0 and diff > threshold):
                anomalous_pts.append(i,i+next_val_to_consider-1,diff)
    elif(what_to_consider == -1):
        for i in range(0,n):
            if(diff<0 and diff < threshold):
                anomalous_pts.append(i,i+next_val_to_consider-1,diff)
    elif(what_to_consider == 0):
        for i in range(0,n):
            if(abs(diff) > threshold):
                anomalous_pts.append(i,i+next_val_to_consider-1,diff)
    '''
    return anomalous_pts
    pass

'''
This function takes 2 arguments:

slopeBasedResult: Result of function "slopeBasedDetection"
any_series: Any CSV in the format of 2 columns (Date,Value), date will be used

Returns array of tuples of the form (start_date,end_date,slope_value)

'''
def anomalyDatesSlopeBaseddetetion(slopeBasedResult,any_series):
    result = []
    for i in range(0,len(slopeBasedResult)):
        start_date = any_series[slopeBasedResult[i][0]][0]
        end_date = any_series[slopeBasedResult[i][1]][0]
        result.append((start_date,end_date,slopeBasedResult[i][2]))
    return result


##########################################################################
##########          TESTING CODE            ##############################
##########################################################################
'''
from Utility import csv2array


wholesale = csv2array('/home/kapil/Desktop/project/library/MumbaiWholesalePriceSmoothed.csv')
retail = csv2array('/home/kapil/Desktop/project/library/MumbaiRetailPriceSmoothed.csv')
wholesale_price = []
retail_price = []
for x in wholesale:
    wholesale_price.append(float(x[1]))

for x in retail:
    retail_price.append(float(x[1]))

anomalies = slopeBasedDetection(wholesale_price,True,retail_price,True,7,True,0,1)

for i in range(0,len(anomalies)):
    start_index = anomalies[i][0]
    end_index = anomalies[i][1]
    slope = anomalies[i][2]
    start_date = wholesale[start_index][0]
    end_date = wholesale[end_index][0]
    print str(start_date) + "," + str(end_date) + "," + str(slope)
'''