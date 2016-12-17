#import pandas as pd
from collections import Counter
import math

data_file = []
data_header = []
data_hdr_list = []
data_file_list = []
data_list = []
outcomeRes = []
data_hdr_entropy = []
entropy_list_attr = {}
entropy_attr_structure = ['Attribute', 'Entropy', 'No. of Rows per attr value', 'Row indices', 'Outcome: Yes, No, Total count']

def readFile():
    global data_hdr_list, data_list 
    with open("./dt-data.txt") as fileReader:
        data_file = fileReader.read().splitlines()
   # print data_file
    data_file.remove("")
    data_header = data_file[0]
    data_file.remove(data_file[0])
    #print data_header
    data_hdr_list = data_header.split(',')
    #print data_hdr_list[0]
    data_hdr_list[0]= data_hdr_list[0].split('(')[1]
    data_hdr_list[-1]= data_hdr_list[-1].split(')')[0]
    
    for i in range(len(data_hdr_list)):
        data_hdr_list[i]= data_hdr_list[i].strip()
    print data_hdr_list
        #print len(data_file)
    for i in range(len(data_file)):
        data_file_list.append([]) 
        data_file_list[i].append(data_file[i])
  #  print "i",i
    i = 0
    data_list = data_file_list
    for data in data_file_list:
        data_list[i] = data[0].split(',')
       # print data_list[i]
        i = i + 1
    for data in data_list:
        #print data[0]
        #print data[-1]
        data[0] = data[0].split(':')[1]
        data[-1] = data[-1].split(';')[0]
        #print data[0]
       # print data[-1]
    for j in range(len(data_list)):
        #print data_list[j]
       # print "len", len(data_list[j])
        for k in range(len(data_list[j])):
            data_list[j][k] = data_list[j][k].strip()
            
    for data in data_list:
        #for dat in data:
        print data

def findEntropyOutcome(attrName,attrIndex):
    global outcomeRes
    print attrName, attrIndex
    for data in data_list:
        outcomeRes.append(data[attrIndex])
    print outcomeRes
    count = Counter(outcomeRes)
    yesCount = count['Yes']
    noCount = count['No']
    print yesCount, noCount
    totalCount = len(outcomeRes)
    print totalCount
    entropyOutcome = (((float(yesCount)/totalCount) * math.log((float(totalCount)/yesCount),2) + ((float(noCount)/totalCount)* math.log((float(totalCount)/noCount),2))))
    print entropyOutcome
    return entropyOutcome

    
def findEntropy(attrName, attrIndex):
    global entropy_list_attr
    temp_list_yes_no  = []
    temp_list_counter = []
    ase = []
    print attrName, attrIndex
    #outcomeRes = []
    #for data in data_list:
     #   outcomeRes.append(data[-1])
   # print "Enjoy:",outcomeRes
    outcome = []
    for data in data_list:
        outcome.append(data[attrIndex])
    #print outcome
    count = Counter(outcome)
    #entropy_list_loc.append(count)
    print count
    branchList = []
    for c in count:
        branchList.append(c)
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
            entropyOutcome = float(entropyOutcome) + ((float(probCount)/totalCount)*(((float(yesCount)/probCount) * math.log((float(probCount)/yesCount),2) 
                                                                                      + ((float(noCount)/probCount)* math.log((float(probCount)/noCount),2)))))
            #print entropyOutcome
            i = i+1
    #st = [item for item in st if item!= []]
    #print st
    #print temp_list_yes_no
    #entropy_list_loc.append()
    entropy_list_attr.update({attrName:([attrName,entropyOutcome, branchList, count, ase, temp_list_yes_no])})
    print entropyOutcome
    return entropyOutcome
                
class TreeNode(object):

   # name = 'Default'
   # entropy = 0.0
    #downLinks = []
    #branchList = []
    #nodeType = None # 'A' - for attribute  ;  'V' - value/branch node
    #upLink = None
    #visited = None
    #attrChosen = {}
    #data = []
    def __init__(self,nodeName, data = None, attrDict =None, entropy = 0.0, branchList = None, upLink = None, nodeType):
        self.name     = nodeName
        self.entropy  = entropy
        self.upLink   = upLink
        self.downLinks = []
        self.NodeType = nodeType
#        if branchList is None:
#            self.nodeType = 'V'
#        else:
        
        if self.nodeType == 'A':   
            self.branchList = branchList
            self.attrChosen = attrDict.copy()
            self.data = data
            for branch in branchList:
                self.downLinks.append( TreeNode(nodeName = branch, upLink = self , nodeType = 'V') )
                
        

class Tree(object):
    
    rootNode = None
    lastTraversedNode = None
    tempNode = None
    
    def addNode(self, nodeName = None,data = None, entropy = None, branchList = None, whichBranch = None, endOfPath = None):
        
        attrDict = {}
        branchindex = 0
        if self.rootNode is None:
            for attrName in data_hdr_list[:-1]:
                attrDict.update({attrName:False})
            attrDict.update({nodeName:True})
            tempNode = TreeNode(nodeName, data, attrDict, entropy, branchList, upLink = None, nodeType= 'A')
            self.rootNode = tempNode
            self.lastTraversedNode = tempNode
        else:
            valueNode = None
            downlinks = self.lastTraversedNode.downLinks 
            for link in downlinks:
                if link.name == whichBranch:
                    index = branchindex
                    break
                branchindex += 1
            valueNode = downlinks[index]  # ?
            attrDict = self.lastTraversedNode.attrChosen.copy()
            attrDict.update({nodeName:True})
            if branchList is None:
                if endOfPath is None:
                    tempNode =  TreeNode(nodeName, data, attrDict, entropy, branchList, upLink = valueNode, nodeType= 'V')
                else:
                    tempNode =  TreeNode(nodeName, data, attrDict, entropy, branchList, upLink = valueNode, nodeType= 'T')
            else:
                tempNode =  TreeNode(nodeName, data, attrDict, entropy, branchList, upLink = valueNode, nodeType= 'A')
                        
                    
            self.lastTraversedNode = tempNode
            
#            if addToBranch is  None:  # if received an branch Node
#               tempNode = TreeNode(nodeName, entropy, branchList, upLink = self.lastTraversedNode )
#             else:  
#               tempNode = TreeNode(nodeName, entropy, branchList) 
#               selectedBranch = self.lastTraversedNode.downLinks[addToBranch]  #<<<--- Need to return the node whose branchName is passed
#               selectedBranch.downLinks.append( TreeNode(nodeName, entropy, branchList) )# a branch Node will only have 1 Attribute node
               
            
        
        if endOfPath == True:
            self.lastTraversedNode = self.goLevelUp(self.lastTraversedNode)    
            
               
        
    def goLevelUp(self, currentLevelNode):
        if currentLevelNode.uplink.nodeType == 'A':
            return currentLevelNode.upLink.upLink
        if currentLevelNode.uplink.nodeType == 'V':
            return currentLevelNode.upLink 
        
    def printTree(self):
        a = 0   
        currentList = [self]
        while currentList:
            print "level" , a
            childrenList = list()
            for node in currentList:
                print node.name,
                
                if node.dataLinks:
                    childrenList.append(node.left)
                if node.right:
                    childrenList.append(node.right)
            print 
            currentList = childrenList
            a = a + 1
    
    def traverseTree(self, currentNode = rootNode , level = 1):    
        print '(' + currentNode.name + " - " + currentNode.nodeType + " - Level - " + level + ')'
        
        for children in currentNode.downLinks:
            currentNode(children , level+1 )       

    def checkExitTree(self, currentNode = rootNode ):
        
        if currentNode.nodeType == 'T':
            if currentNode.downLinks is None:
                return True
            else:
                return False
        else:
            for children in currentNode.downLinks:
                return ( self.checkExitTree(children) and True)   
                  
#--------------------------------------------------------------------------------------------------------------        
#root = Tree()
readFile()
outcomeEntropyRes = 0
outcomeEntropyRes = findEntropyOutcome(data_hdr_list[-1],-1)
for i in range(len(data_hdr_list)-1):
    data_hdr_entropy.append([])
print data_hdr_entropy
entropyList = []
for i in range(len(data_hdr_list)-1):
    entropyList.append(findEntropy(data_hdr_list[i],i))
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
print  entropy_list_attr
print 
for line in entropy_list_attr:
    print line, entropy_list_attr[line]
    print 
print

rootAttribute = data_hdr_list[indexattr]
root = Tree()
attr2 = data_hdr_list[0]
branchList = entropy_list_attr[rootAttrobute][2]
root.addNode(rootAttribute,entropy_list_attr[rootAttribute],entropy_list_attr[rootAttribute][1], branchList)
branches = entropy_list_attr[attr2][2]
for branch in branchList:
    root.addNode(attr2, entropy_list_attr[attr2], entropy_list_attr[attr2][1],branches,branch)


#root.addNodeData(entropy_list_attr[data_hdr_list[indexattr]])
#root.addChosenAttr([],entropy_list_attr[data_hdr_list[indexattr]][0])

#index = 0
#current = root
#parent = None
#for head in data_hdr_list[:-1]:
 #   node = None
  #  if current.IsAttrChosen(head) == False:
   #     #attribute =
    #    current.chooseAttributeNode()
     #   #weightedEntropy = current.calculateEntropy()[1]
      #  parent = current
       # left = Tree(i)
        #left.previous = current
        #current.left = left
        #current = current.left
        #parent = current
        #node = Tree(entropy_list_attr[head])
        #current.left = node
        #node.addChosenAttr(parent.getChosenAttr(),head)
        #current = current.left
        #current.previous = parent
    #index += 1  
    
#root.printTree()
