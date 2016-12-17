#import pandas as pd
from collections import Counter
import math

data_file = []
data_header = []
data_hdr_list = []
data_file_list = []
data_list = []
data_hdr_entropy = []
entropy_list_loc = []
entropy_attr_structure = ['Attribute', 'Entropy', 'No. of Rows per attr value', 'Row indices', 'Outcome: Yes, No, Total count']

def readFile():
    global data_hdr_list, data_list 
    with open("./dt-data.txt") as fileReader:
        data_list = fileReader.read().splitlines()
        
    #remove all spaces + separate headers
    data_hdr_list = ['Row'] + data_list.pop(0)[1:-1].split(', ')
    del data_list[0]
    
    for index in range( len(data_list)):        
        data_list[index] = data_list[index][:-1].replace(': ',', ')
        data_list[index] = data_list[index].split(', ')
  

def findEntropyOutcome(attrName,attrIndex):
    print attrName, attrIndex
    outcome = []
    for data in data_list:
        outcome.append(data[attrIndex])
    print outcome
    count = Counter(outcome)
    yesCount = count['Yes']
    noCount = count['No']
    print yesCount, noCount
    totalCount = len(data_list)
    print totalCount
    entropyOutcome = (((float(yesCount)/totalCount) * math.log((float(totalCount)/yesCount),2) + ((float(noCount)/totalCount)* math.log((float(totalCount)/noCount),2))))
    print entropyOutcome
    return entropyOutcome

    
def findEntropy(attrName, attrIndex):
    global entropy_list_loc
    temp_list_yes_no  = []
    temp_list_counter = []
    ase = []
    print attrName, attrIndex
    outcomeRes = []
    for data in data_list:
        outcomeRes.append(data[-1])
   # print "Enjoy:",outcomeRes
    outcome = []
    for data in data_list:
        outcome.append(data[attrIndex])
    #print outcome
    count = Counter(outcome)
    #entropy_list_loc.append(count)
    print count
    for c in count:
        ase.append(c)
        ase.append([i for i, x in enumerate(outcome) if x == c])
    print ase
    #entropy_list_loc.append(ase)
    st = []
    totalCount = len(data_list)
    entropyOutcome = 0
    for i in range(len(ase)):
        st.append([])
        if i % 2 == 0:
            for j in ase[i+1]:
                st[i].append(outcomeRes[j])
       #     print "outcome for attribute value", ase[i],st[i]
            count2 = Counter(st[i])
            yesCount = count2['Yes']
            noCount = count2['No']
            probCount = yesCount + noCount
            temp_list_yes_no.append([yesCount,noCount,probCount])
            temp_list_counter.append(ase[i])
     #       print yesCount, noCount
      #      print probCount, totalCount
            entropyOutcome = float(entropyOutcome) + (float(probCount)/totalCount)*(((float(yesCount)/probCount) * math.log((float(probCount)/yesCount),2) + ((float(noCount)/probCount)* math.log((float(probCount)/noCount),2))))
            #print entropyOutcome
            i = i+1
    #st = [item for item in st if item!= []]
    #print st
    #print temp_list_yes_no
    #entropy_list_loc.append()
    entropy_list_loc.append([attrName,entropyOutcome,count, ase, temp_list_yes_no])
    print entropyOutcome
    return entropyOutcome


#--------------------------------------- Driver Program ----------------------------------------------- 
   
readFile()
outcomeEntropyRes = 0
outcomeEntropyRes = findEntropyOutcome(data_hdr_list[-1],-1)
for i in range(len(data_hdr_list)-1):
    data_hdr_entropy.append([])
print data_hdr_entropy
entropyList = []
for i in range(len(data_hdr_list)-1):
    entropyList.append(findEntropy(data_hdr_list[i+1],i+1))
print "outcome entropy of result", outcomeEntropyRes
print data_hdr_list[:len(data_hdr_list)-1]
print "individual weighted entropy", entropyList[-1]
diffEntropy = []
diffEntropy[:] = [outcomeEntropyRes-e for e in entropyList]
print "Difference between outcome and attribute entropy",diffEntropy
indexattr = diffEntropy.index(max(diffEntropy))
print "attribute with highest information gain",max(diffEntropy), data_hdr_list[indexattr], "column"
print
print
print "list containing entropy, count details for all attributes"
for e in entropy_attr_structure:
    print e," | ",
print 
for line in entropy_list_loc:
    for row in line:
        print row
    print