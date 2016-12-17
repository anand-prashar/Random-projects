'''
Created on Sep 28, 2016

@author: anand
'''

global myFirstDict

def getWordCountUsingDict(s):
    
    myFirstDict = dict()
    
    for ch in s:
        if ch not in myFirstDict:
            myFirstDict[ch] = 1
        else:
            myFirstDict[ch] = myFirstDict[ch] + 1
                
    return myFirstDict

    
def inOperatorOnKey():
    if 'k1' in myFirstDict:
        print(myFirstDict['k1'])
    else:
        print('Key doesnt exist')    

def inOperatorOnValue():
    val = 'val1'
    valList = myFirstDict.values()
    
    #look in values list
    if val in valList:  
        print('value exists')
    else:
        print('Value doesnt exist')       

def wordCount():
    fname = raw_input('Enter the file name: ')
    try:
        fhand = open(fname)
    except:
        print 'File cannot be opened:', fname
        exit()
    counts = dict()
    for line in fhand:
        words = line.split()
    for word in words:
        if word not in counts:
            counts[word] = 1
    else:
        counts[word] += 1
    print counts
    
def printDict():
    
    for tpl in myFirstDict:
        print tpl, myFirstDict[tpl]
        
            

#--------------------------------------------------------

myFirstDict = dict()
print myFirstDict

myFirstDict['k1'] = 'value1'
myFirstDict['k2'] = 'value2'
#print myFirstDict

#myTempDict = getWordCountUsingDict('This is This is all');
#print myTempDict

#inOperatorOnKey()
#inOperatorOnValue()

printDict()
