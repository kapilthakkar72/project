import csv
import sklearn
import numpy as np
from sklearn import  linear_model
import matplotlib.pyplot as plt
from scipy.stats import norm


# Reading arrival from csv
arrival = []
with open('arrival.csv', 'rb') as csvfile:
    arrivalreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in arrivalreader:
        arrival.append([float(str(row[0]))])
        
# Reading WP from csv
wholesale = []
with open('wholesale.csv', 'rb') as csvfile:
    wpreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in wpreader:
        wholesale.append([float(str(row[0]))])

# Reading retail from csv
retail = []
with open('retailprice.csv', 'rb') as csvfile:
    retailreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in retailreader:
        retail.append([float(str(row[0]))])
        
        
arrival = np.array(arrival)
wholesale = np.array(wholesale)
retail = np.array(retail)
        
# Split the arrival into training/testing sets
arrival_train = arrival[:-20]
arrival_test = arrival[-20:]

# Split the wholesale into training/testing sets
wholesale_train = wholesale[:-20]
wholesale_test = wholesale[-20:]


retail_train = retail[:-20]
retail_test = retail[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

print len(arrival_train)
print len(wholesale_train)

print arrival_train.shape

# Train the model using the training sets
# regr.fit(wholesale_train, retail_train)
regr.fit(arrival_train, wholesale_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(arrival_test) - wholesale_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(arrival_test, wholesale_test))

# Plot outputs
# plt.scatter( wholesale_train, retail_train,  color='black')
plt.scatter( arrival_train, wholesale_train,  color='black')
# plt.plot(wholesale_train, regr.predict(wholesale_train), color='blue',linewidth=3)
plt.plot(arrival_train, regr.predict(arrival_train), color='blue',linewidth=3)
# 
# 
plt.xticks(())
plt.yticks(())

plt.show()


aboveLine = []

for i in range(0,len(wholesale_train)):
    x = retail_train[i] - regr.predict(wholesale_train[0])
    if(x[0] > 0):
        aboveLine.append(x[0])


# rv = norm()
# fig, ax = plt.subplots(1, 1)
# ax.plot(aboveLine, rv.pdf(aboveLine), 'k-', lw=2, label='frozen pdf')
# plt.hist(aboveLine,bins=30)
# plt.show()
