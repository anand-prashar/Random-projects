'''
Created on Oct 5, 2016

@author: anand
'''

import numpy as np
import numpy.linalg as LA # numpy's linear algebra package
from numpy import double



def readFile():
    
    try:
        fHandle = open('pca-data.txt')
    except:
        #print 'Data fetch error'
        exit()
    
    dataList = []    
    for line in fHandle:
        
        listOfRow =  line.split('\t')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        dataPoint = np.matrix( [ [ double( listOfRow[0])] , 
                                 [ double( listOfRow[1])] , 
                                 [ double( listOfRow[2])] ] )
        dataList.append( dataPoint )
        
    return dataList

    
def normalizeVectors(dataList):
     
    meanVector = np.matrix([ [0.0], 
                             [0.0], 
                             [0.0] ])  # need as Nx1 matrix
    #print 'shape:', meanVector.shape
    for dataVector in dataList:
        meanVector += dataVector
    meanVector =  meanVector/len(dataList)
    
    for dataVector in dataList:
        dataVector -= meanVector
    
    #print meanVector  
    return dataList 
    

def findCovariance(dataList):
    
    # each data point is a 3x1 matrix. Its transpose will be 1x3 matrix. So we need 3x3 matrix to hold product and coVariance
    transposeSum = np.matrix( [ [ double( 0.0) , double( 0.0) , double( 0.0) ],
                                [ double( 0.0) , double( 0.0) , double( 0.0) ],
                                [ double( 0.0) , double( 0.0) , double( 0.0) ]  
                            ] )
    
    for dataVector in dataList:
        transposeProduct = dataVector * (dataVector.getT()) # (matrix X matrix) transpose
        transposeSum+= transposeProduct
    
    #print transposeSum
    #print 'shape:', transposeSum.shape
    sigma = transposeSum / len(dataList)
    
    return sigma    
        
def calcEigenValuesNVectors(coVariance):
    eVal, eVect = LA.eig(coVariance)
    #print 'EIGEN VALUE AND VECTOR = \n',eVal
    #print '\n\n', eVect
    #u, s, v = LA.linalg.svd(coVariance, full_matrices = True)
    ##print '\n\nSVD: U S V-\n', u, '\n',s,'\n',v
    return eVect

def calcDimensionRedction(eigenVector, dataList, K):
    
    
    # Need to clip 1st K columns-- to create zMatrix :
    # 1st, transpose the matrix.. so we can easily clip from a array
    # after clipping, re-transpose to place it back in order
    UReduceMatrix = eigenVector.getT()  
    UReduceMatrix = UReduceMatrix[:K]
    UReduceMatrix = UReduceMatrix.getT()
    
    #UReduceMatrix = UReduceMatrix transpose ( because we need this to multiply to all data points)
    #could have saved a transpose operation, but following the steps for learning
    UReduceMatrix = UReduceMatrix.getT()
    
    writeToFile = open('PCA_Output_Anand_and_Vijay.txt', 'w')
    
    for dataPoint in dataList:
        strResultLine = UReduceMatrix*dataPoint
        strResultLine = str(strResultLine[0][0])[3:-2]+',\t'+str(strResultLine[1][0])[3:-2]+'\n'
        
        writeToFile.write(strResultLine)
        #print strResultLine
        #strResultLine.replace(old, new)
    writeToFile.close()
    print 'Success : Output file- PCA_Output_Anand_and_Vijay.txt'
        
dataList = readFile()
dataList = normalizeVectors(dataList )  
coVariance = findCovariance(dataList)
eigenVector = calcEigenValuesNVectors(coVariance)
result = calcDimensionRedction(eigenVector, dataList, K=2)
