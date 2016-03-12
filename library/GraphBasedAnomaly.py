import numpy
from math import exp
from numpy import linalg as LA
from numpy import matrix

# Similarity Measure using RBF Function
'''
This function takes 2 arguments:
X : Array of arrays
sigma : Tunable parameter, by default 1

Explanation:

As this function is used to calculate similarity measure among multiple timeseries, X is list of lists.
Where each list inside X, represents 1 series.

sigma is parameter used in rbf function:

    K(i,j) = exp(- (Sum of (k=1 to p))(x.ki - x.kj)^2 / sigma^2)
    
Where p is number of series

Returns 2D Metrix, where each cell (i,j) is similarity measure calculated using above formula.

Requirements : Length of each series should be same
'''
def rbfSimilarity(X, sigma=1):
    numOfSeries = len(X)
    # Length of each series
    n = len(X[0])
    
    # Generates 2D array of size n*n, each element is set to zero
    K = numpy.empty((n,n))
    K.fill(0)
    
    for i in range(0,n):
        for j in range(0,n):
            temp = 0
            for p in range(0,numOfSeries):
                temp += (X[p][i] -X[p][j])*(X[p][i] -X[p][j])
            temp = 0-temp
            temp = temp / (sigma * sigma)
            K[i][j] = exp(temp)
            
    return K

'''
This function takes 2D square matrix as input and returns its (eigenvalues,eigenvectors)
'''
def eigenVectors(K):
    # Returns eigenvalues and right eigenvectors of a square array.
    eigenvalues,eigenvectors = LA.eig(K)
    return (eigenvalues,eigenvectors)

'''
This is helper function used in weights() function to calculate complex numerator
'''
def numeratorForWeights(v,Ky):
    # Length of eigenvectors
    n = len(v)
    v = numpy.array(v)[numpy.newaxis]
    vt = v.transpose()
    vvt = v * vt
    frobeniusInnerProduct = 0
    for i in range(0,n):
        for j in range(0,n):
            frobeniusInnerProduct += (vvt[i][j] * Ky[i][j])            
    return frobeniusInnerProduct
        

'''
Given eigenvalues, eigenvectors and Ky, calculates weight parameters alpha-i
'''
def weights(eigenvalues, eigenvectors, Ky, mu = 1):
    # Number of weights
    n = len(eigenvalues)
    # Initialising array
    alpha = numpy.empty(n)
    alpha.fill(0)
    # Calculating each element
    for i in range(0,n):
        alpha[i] = eigenvalues[i] + (numeratorForWeights(eigenvectors[i],Ky)) / (2*mu)
    return alpha

'''
This function takes weights and eigenvectors as input and retuns aligned kernel matrix Ka
'''
def alignedKernelMatrix(alpha, eigenvectors):
    # Get how many rows
    n = len(eigenvectors)
    Ka = numpy.empty((n,n))
    Ka.fill(0)
    
    for i in range(0,n):
        Ka += (alpha[i] * eigenvectors * eigenvectors.transpose())
    return Ka

'''
This function shifts elemenst of matrices so that it does not have any negative value in it.
'''
def shiftToRemoveNegativeVals(Ka):
    minElement = Ka.min()
    return (Ka + abs(minElement))

'''
Aligns two kernels Kx and Ky and returns Ka, aligned matrix.
Where Kx is predictor variable and Ky is target variable.
Kx and Ky are kernel matrices, obtained by applying similarity function.
'''

def kernelAlignment(Kx,Ky):
    # Get eigenvalues and eigenvectors of Kx
    (eigenvalues,eigenvectors) = eigenVectors(Kx)
    # Get weights
    alpha = weights(eigenvalues, eigenvectors, Ky)
    # Get aligned kernel matrix
    Ka = alignedKernelMatrix(alpha, eigenvectors)
    Ka = shiftToRemoveNegativeVals(Ka)
    return Ka

'''
This function normalises matrix K and returns normalised Kernel matrix
'''
def normalise(K):
    n = len(K)
    # Get sum of all columns for normalising
    sumOfCols = numpy.empty(n)
    sumOfCols.fill(0)    
    for j in range(0,n):
        for i in range(0,n):
            sumOfCols[j] += K[i][j]    
    for i in range(0,n):
        for j in range(0,n):
            K[i][j] = K[i][j] / sumOfCols[j]
    return K

    