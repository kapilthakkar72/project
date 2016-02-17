import numpy
import math
import matplotlib.pyplot as plt

'''
This function takes 5 arguments:
arr1: Series 1
arr2: Series 2
maxlag: maximum lag to consider
pos: to take potitive lag or not, i.e. 1 to maxlag
neg: to take negative lag or not, i.e. -maxlag to -1

Returns an array containing tuples of the form (lag, correlation at this lag)

Requirements: Length of both the series should be equal
'''
def correlation(arr1, arr2, maxlag, pos=1, neg=1):
    # Will contain tuples (lag, correlation)
    result = []
    
    # Checking for requirements
    if(len(arr1) != len(arr2)):
        print "Error! In Function: correlation(arr1, arr2, maxlag, pos=1, neg=1): \n Length of the both series should be same. Returning empty result. \n"
        return result
    
    # Mean of the two series
    mean1 = numpy.mean(arr1)
    mean2 = numpy.mean(arr2)
    
    # Calculating the denominator
    sx = 0
    sy = 0
    for i in range(0,len(arr1)):
        sx += (arr1[i] - mean1) * (arr1[i] - mean1)
        sy += (arr2[i] - mean2) * (arr2[i] - mean2)
    denom  = math.sqrt(sx * sy)
    
    # Getting max and min lag
    maxLag = maxlag         # Default: Both sides are to be considered
    minLag = -maxlag
    if(pos==1 and neg ==0):
        minLag = 0
    elif(pos==0 and neg ==1):
        maxlag = 0
    
    # Calculate correlation at multiple lags
    lag = 0
    for lag in range(minLag,maxlag+1):
        sxy = 0
        for i in range(0,len(arr1)):
            j = i + lag
            if(j<0 or j>= len(arr1)):
                continue
            else:
                sxy += (arr1[i] - mean1) * (arr2[j] - mean2)
        r = sxy / denom
        result.append((lag,r))
        
    return result

'''
This function takes 2 arguments:
arr1: Series of the form (lag,correlation)
positive_correlation: true if we are looking for maximum positive correlation, else false

Returns a tuple of the form (lag,correlation), where correlation value is the maximum or minimum of the array depending on positive_correlation parameter.
Lag is the lag value at which we found max/min correlation value
'''
def getMaxCorr(arar1,positive_correlation):
    if(positive_correlation == True):
        (maxLag,corr) = arar1[0]
        for (lag, correlation) in arar1:
            if(corr < correlation):
                (maxLag,corr) = (lag, correlation)
        return (maxLag,corr)
    else:
        (minLag,corr) = arar1[0]
        for (lag, correlation) in arar1:
            if(corr > correlation):
                (minLag,corr) = (lag, correlation)
        return (minLag,corr)

'''
This function takes 7 arguments:
arr1: Series 1
arr2: Series 2
maxlag: maximum lag to consider
positive_correlation: true if we are looking for maximum positive correlation, else false
pos: to take potitive lag or not, i.e. 1 to maxlag
neg: to take negative lag or not, i.e. -maxlag to -1
window_size: window size to consider while calculating sliding window correlation

Returns an array containing tuples of the form (lag, max/min correlation at this window) for all windows.
Note that window number can easily be implied by the index of that tuple in resultant array.

Requirements: Length of both the series should be equal
'''
def window_correlation(arr1, arr2, maxlag,window_size=15, positive_correlation=True , pos=1, neg=1):    
    # Will contain tuples (lag, correlation)
    result = []
    
    # Checking for requirements
    if(len(arr1) != len(arr2)):                            
        print "Error! In Function: correlation(arr1, arr2, maxlag, pos=1, neg=1): \n Length of the both series should be same. Returning empty result. \n"
        return result
    
    # Length of array
    n = len(arr1)
    
    if(window_size >= n):
        temp = correlation(arr1,arr2,maxlag,pos,neg)
        # Get maximum correlation
        result.append(getMaxCorr(temp,positive_correlation))
    else:
        for i in range(0,n-window_size):
            # Take out one window and find correlation
            temp_arr_1 = arr1[i:(i+window_size)]
            temp_arr_2 = arr2[i:(i+window_size)]
            temp = correlation(temp_arr_1,temp_arr_2,maxlag,pos,neg)
            # Get maximum correlation and append it to array
            result.append(getMaxCorr(temp,positive_correlation))
    return result

'''
arr: array of tuples of the form (lag,correlation) for each window.

Number of windows = size of an array

Plots correlation at each window
'''
def plotWindowCorr(arr):
    # Extract Correlation values of each window
    y_vals = [x[1] for x in arr]
    # x_vals is nothing but window number
    x_vals = list(xrange(1,len(arr)+1))
    plt.plot(x_vals,y_vals)    
    plt.show()


######################################################################
##                       TESTING CODE                               ##
######################################################################
import random

a = [random.randint(1,100) for _ in range(50)]
b = [random.randint(1,100) for _ in range(50)]

arr = window_correlation(a,b,10)
plotWindowCorr(arr)