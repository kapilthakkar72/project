# R Code

# This is just sample code to examine outlier anomaly

library(stats)
library(base)
library(randomWalkAnomaly)
# Example 1
Input = matrix(c(0,0.3,0.4,0,0.3,0,0.5,0,0.4,0.5,0,0,0,0,0,0),4,4)
Input
outlierAnomaly(Input,0.2,0.2)

# Generating Similarity Measure Matrix

library(multivariateAnomaly)
data(KernelData)
TimeSeries = as.matrix(KernelData)

# Columns represent timestamp
# Rows represent real valued variable

TimeSeries

RBFMeasure(TimeSeries,1.414)        # Radial Basis Function (RBF)

# Generating Kernel Matrix

library(matrixcalc)
TempA = data(FrobeniusA)
TempB = data(FrobeniusB)
A = as.matrix(FrobeniusA)
B = as.matrix(FrobeniusB)