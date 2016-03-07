import numpy
import sklearn
import numpy as np
from sklearn import  linear_model
import matplotlib.pyplot as plt
from scipy.stats import norm
from Utility import MADThreshold
'''
This function takes 5 arguments:
x_series: independent variable
y_series: dependent variable : y = f(x)
param: Defines what to be treated as anomaly depending on its value as follows:
        0: Values going out of range, both with positive and negative error
        1: Values with potitive errors
        -1: Values with negative errors
default_threshold: Whether to use default threshold used by system using MAD test or user defined threshold
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
    # print "x_series"
    # print x_series
    # print "y_series"
    # print y_series
    x_series = np.array(x_series)
    y_series = np.array(y_series)
    x_series = x_series.reshape(len(x_series),1)
    y_series = y_series.reshape(len(y_series),1)
    print x_series
    print x_series.shape
    print y_series.shape
    # Create linear regression object
    regr = linear_model.Lars()
    # Train the model using the training sets
    regr.fit(x_series, y_series)
    # Plot outputs
    # plt.scatter( x_series, y_series,  color='black')
    # plt.plot(x_series, regr.predict(x_series), color='blue',linewidth=3)
    # plt.xticks(())
    # plt.yticks(())
    # plt.show()
    
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
        (_,outVal)=  MADThreshold(diff)
    else:
        outVal = threshold
    
    results = []
    for i in range(0,len(diff)):
        if(diff[i][4] > outVal):
            results.append(diff[i])
    print "DIFF:"
    print diff
    return (results,regr)

'''
This function takes 2 arguments:

result_of_lr: Result of function "linear_regression"
any_series: Any CSV in the format of 2 columns (Date,Value), date will be used

Returns array of tuples of the form (start_date,x_value,y_value,predicted_y_value,difference_between_predicted_and_actual_y_value)

'''
def anomalies_from_linear_regression(result_of_lr, any_series):
    result = []
    print "RESULT OF LR"
    print result_of_lr
    #print "Check 1"
    for i in range(0,len(result_of_lr)):
        #print "Check 2"
        #print "First : " + str(result_of_lr[i][0])
        #return result
        start_date = any_series[result_of_lr[i][0]][0]
        result.append((start_date,result_of_lr[i][1],result_of_lr[i][2],result_of_lr[i][3],result_of_lr[i][4]))
    return result
