import numpy
import numpy as np
import csv

'''
This function takes one argument:
array: Array of integers, real numbers, etc

returns threshold value to be consider using MAD Test
'''
def MADThreshold(array):
    # return 1.4826*numpy.median(np.array(array))
    array = np.array(array)
    median = numpy.median(array)
    diff = []
    for i in range(0,len(array)):
        diff.append(abs(median - array[i]))
    median_of_diff = numpy.median(np.array(diff))
    tolerance = 1.4826 * median_of_diff
    return (median - tolerance,median + tolerance)
    

'''
This function takes 2 arguments:
array: Array of integers, real numbers, etc
alpha: smoothening factor of exponential average smoothing

returns threshold value to be consider using MAD Test
'''
def smoothArray(array, alpha = 2.0/15.0):
    array = np.array(array,dtype = float)
    if(len(array) == 0):
        return []
    new_data = []
    prevVal = -1
    prevVal = array[0]
    new_data.append(array[0])
    for i in range(1,len(array)):
        newVal = ( array[i] - prevVal ) * alpha + prevVal
        new_data.append(newVal)
        prevVal = newVal   
    return new_data

def csv2array(filePath):
    result = []
    with open(filePath, 'rb') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        for row in csvReader:
            result.append(row)
    return result

def getColumn(array, column_number):
    temp = []
    for x in array:
        temp.append(x[column_number])
    return temp

'''
While reading CSV file, by default it takes each row as string, but second column should be float, so this function does that work.

1 Argument:

z : Array from CSV file consisting of 2 columns, date and values
return same array changing data type of second column to float

'''
def formatCSV2Array(z):
    result = []
    for row in z:
        result.append((row[0],float(row[1])))
    return result
