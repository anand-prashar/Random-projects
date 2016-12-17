'''
Created on Sep 23, 2016

@author: vijay
'''
from random import randrange
import math
import numpy as np

data_file = []
data_points = []
centroids = []
centroidData = []
clusterNumber = 3
prevCentroids = []
prevData = []

gaussianData = []
prevMeans = []
prevAmplitude = []
prevCoVarianceMat = []
prevCoVarianceDet = []
covarMan = []
gaussDist = []
prevGaussDist = []
covarMatrixDet = []
coVarMatrix = []

def readFile():
    global data_file
    data_point = []
    with open("./clusters.txt") as fileReader:
        data_file = fileReader.read().splitlines()
    for d in data_file:
        data_point = d.split(",")
        data_points.append([float(data_point[0]),float(data_point[1])])
        
def getInitialCentroids(clusterNo):
    mean = []
    for i in range(0,clusterNo):
        randIndex = randrange(0,len(data_points))
        mean.append(data_points[randIndex])
    return mean

def assignPointsToCluster(pointIndex, point):
    global centroidData
    distances = []
    for centroid in centroids:
        distances.append(calculateDistance(point,centroid))
    argmin = distances.index(min(distances)) # centroid number
    centroidData[argmin].append(pointIndex)
    
    
def calculateDistance(point, centroid):
    return math.pow(point[0]-centroid[0], 2) + math.pow(point[1]-centroid[1], 2)
    

def findNewCentroid(cluster):
    global centroids
    list_x = []
    list_y = []
 
    for point in cluster:
        list_x.append(data_points[point][0])
        list_y.append(data_points[point][1])
    x_mean = float("{0:.9f}".format(sum(list_x) / float (len(list_x))))
    y_mean = float("{0:.9f}".format(sum(list_y) / float (len(list_y))))
    centroids.append([x_mean,y_mean])
    
def findDistmultivariate(x, mean, covarmatrix, covmatdet):
    denom_constant = 1.0/ ( math.pow((2*math.pi),float(2)/2) * math.pow(covmatdet,1.0/2) )
    x_mean_diff = np.matrix(x - mean)
    inv = covarmatrix.I 
    #print "dimensions", x_mean_diff.shape,  inv.shape, (x_mean_diff.T).shape
    expValue = math.pow(math.e, -0.5 * np.linalg.det(np.matmul(np.matmul(x_mean_diff, inv), x_mean_diff.T )))
    return denom_constant * expValue

def findGuassianX():
    global gaussDist
    localList = []
    for point in data_points:
        i = 0
        while i < len(centroids):
            gauss = findDistmultivariate(np.matrix(point), centroids[i], np.matrix(coVarMatrix[i]), covarMatrixDet[i])
            localList.insert(i, amplitude[i] * gauss)
            i+=1
        #print localList
        sum_gauss = sum(localList)
        ric = [x/float(sum_gauss) for x in localList]
        gaussDist.append(list(ric))
        del localList[:]
        del ric[:]

def findNewMeanandCovariance():
    global centroids, amplitude, covarMan, coVarMatrix, covarMatrixDet
    list_x = []
    list_y = []
    mat_x = []
    mat_y = []
    k = 0
    while k < len(prevMeans):
        i = 0
        while i < len(data_points): 
            list_x.append(data_points[i][0] * gaussDist[i][k])
            list_y.append(data_points[i][1] * gaussDist[i][k])
            mat_x.append(data_points[i][0])
            mat_y.append(data_points[i][1])
            i+=1
        newLen = sum(np.array(gaussDist)[:,k])
        amplitude.append(float("{0:.9f}".format(float(newLen)/len(data_points))))
        x_mean = float("{0:.9f}".format(sum(list_x) / float (newLen)))
        y_mean = float("{0:.9f}".format(sum(list_y) / float (newLen)))
        centroids.append([x_mean,y_mean])
        i = 0
        covarInd = []
        while i < len(data_points):
            covarInd.append(findCovariance(np.matrix([mat_x[i],mat_y[i]]).T,np.matrix(centroids[k]).T, gaussDist[i][k]))
            i+=1
        sum1 = sum(covarInd)
        covarMan.append(sum1 / newLen)
        #print covarMan
        k+=1
        del list_x[:], list_y[:], mat_x[:], mat_y[:]
        
    coVarMatrix = list(covarMan)
    for var in coVarMatrix:
        covarMatrixDet.append(np.linalg.det(var))
        
def findCovariance(arrayMat, mean,ric = 1):
    mat = np.matrix(arrayMat-mean)
    matTranspose = mat.T
    #print mat.shape, matTranspose.shape
    resMatrix = np.matmul(mat, matTranspose)
    resMatrix = resMatrix * ric
    return resMatrix

#####################################################################################################################

readFile()
centroids = getInitialCentroids(clusterNumber)
print "Centroids chosen initially:"
for c in centroids:
    print "Point ", c
    centroidData.append([])
i = 0
for point in data_points:
    assignPointsToCluster(i, point)
    i+=1

for data in centroidData:
    if len(data) ==0:
        index = centroidData.index(data)
        centroidData.remove(data)
        centroids.remove(centroids[index])
if len(centroids) != clusterNumber:
    print "New centroids after no data points were assigned to one or more centroids:"
    for c in centroids:
        print "Point ", c

print "\n\nNew Centroids: "
runAlgo = True
iterations = 0

while runAlgo:
    iterations+=1
    prevCentroids = list(centroids)
    prevData = list(centroidData)
    del centroids[:]
    for cluster in centroidData:
        findNewCentroid(cluster)
    del centroidData[:]
    print "Iteration: ", iterations+1  
    for c in centroids:
        print "Point ",c
        centroidData.append([])
    print 
    #index = 0
    if prevCentroids == centroids:
        print "Converged. Clusters finalized. Total iterations taken: ", iterations 
        runAlgo = False
        break
    i = 0
    for point in data_points:
        assignPointsToCluster(i, point)
        i+=1
    for data in centroidData:
        if len(data) == 0:
            index = centroidData.index(data)
            centroidData.remove(data)
            centroids.remove(centroids[index])
    if len(centroids) != clusterNumber:
        print "New centroids after no data points were assigned to one or more centroids:"
        for c in centroids:
            print "Point ", c
        print
        
#Gaussian MM

for dataindices in prevData:
    gaussianData.append([data_points[x] for x in dataindices])
data_array = np.array(gaussianData)

#for array in data_array:
#   covarStd.append(np.cov(np.array(array).T))
k = 0

while k < len(centroids):
    covarMan.append(findCovariance(np.matrix(data_array[k]).T,np.matrix(centroids[k]).T)/len(data_array[k]))
    k+=1
coVarMatrix = list(covarMan)

for var in coVarMatrix:
    covarMatrixDet.append(np.linalg.det(var))

amplitude = list([float("{0:.9f}".format(float(len(x))/len(data_points))) for x in gaussianData])

#print amplitude
print "\nGaussian Mixture Model initialized with K- Means clusters\n"
index = 0
while index < len(centroids):
    print "Cluster ", index +1, " : "
    print "Mean (Co-ordinates) = ", centroids[index]
    print "Co-variance Matrix: ", coVarMatrix[index]
    print "Amplitude: ", amplitude[index],"\n"
    index+=1
    
print "New Values of Mean, Co-Variance and Amplitude\n"

runAlgo = True
z = 0

while runAlgo:
    prevGaussDist = list(gaussDist) 
    del gaussDist[:]
    
    findGuassianX()
    
    prevMeans = list(centroids)
    prevCoVarianceMat = list(coVarMatrix)
    prevCoVarianceDet = list(covarMatrixDet)
    prevAmplitude = list(amplitude)
     
    del centroids[:], amplitude[:], coVarMatrix[:], covarMatrixDet[:]
    
    findNewMeanandCovariance()
    
    if prevMeans == centroids and prevAmplitude == amplitude:#prevCoVarianceDet == covarMatrixDet prevCoVarianceMat == coVarMatrix and 
        print "Converged. Clusters finalized. Total iterations taken: ", z+1
        runAlgo = False
        break
    print "Iteration = ", z+1
    index = 0
    while index < len(centroids):
        print "Cluster ", index +1, " : "
        print "Mean (Co-ordinates) = ", centroids[index]
        print "Co-variance Matrix: ", coVarMatrix[index]
        print "Amplitude: ", amplitude[index],"\n"
        index+=1
    z+=1