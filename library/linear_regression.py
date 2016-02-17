import numpy
import sklearn
import numpy as np
from sklearn import  linear_model
import matplotlib.pyplot as plt
from scipy.stats import norm

'''
This function takes 5 arguments:
x_series: independent variable
y_series: dependent variable : y = f(x)
param: Defines what to be treated as anomaly depending on its value as follows:
        0: Values going out of range, both with positive and negative error
        1: Values with potitive errors
        -1: Values with negative errors
default_threshold: Whether to use default threshold used by system using MOD test or user defined threshold
threshold: Threshold value if it is used defined and default_threshold is 'False'

returns Following tuple:

(result,regression_object)

    1. returns "results" array of tuples which are anomaly according to linear regression test of following format:
        Tuple:(Index of Data Point,x_value,y_value,predicted_y_value,difference_between_predicted_and_actual_y_value)
        
    2. regression_object which can be used to regenerate predicted values for plotting graphs afterwards
       Format of using: regression_object.predict(x_value)

Requirements: Length of both the series should be equal
'''
def linear_regression(x_series, y_series, param = 0, default_threshold = True, threshold = 0):
    # Create linear regression object
    regr = linear_model.Lars()
    # Train the model using the training sets
    regr.fit(x_series, y_series)
    # Plot outputs
    plt.scatter( x_series, y_series,  color='black')
    plt.plot(x_series, regr.predict(x_series), color='blue',linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()
    
    # Array to store differences between original and predicted
    diff = []

    for i in range(0,len(x_series)):
        x = y_series[i] - regr.predict(x_series[i])
        x = (i,x_series[i],y_series[i],regr.predict(x_series[i]),x)
        if(param == 0):
            diff.append(abs(x))
        elif(param == 1 and x>0):
            diff.append(x)
        elif(param == -1 and x<0):
            diff.append(x)
    
    # Finding outliers
    if(default_threshold == True):
        outVal=  1.4826*numpy.median(numpy.array(diff))
    else:
        outVal = threshold
    
    results = []
    for i in range(0,len(diff)):
        if(diff[i][4] > outVal):
            results.append(diff[i])
    return (results,regr)
