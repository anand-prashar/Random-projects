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
    data_file.remove("")
    data_header = data_file[0]
    data_file.remove(data_file[0])
    data_hdr_list = data_header.split(',')
    data_hdr_list[0]= data_hdr_list[0].split('(')[1]
    data_hdr_list[-1]= data_hdr_list[-1].split(')')[0]
    
    for i in range(len(data_hdr_list)):
        data_hdr_list[i]= data_hdr_list[i].strip()
    for i in range(len(data_file)):
        data_file_list.append([]) 
        data_file_list[i].append(data_file[i])
    i = 0
    data_list = data_file_list
    for data in data_file_list:
        data_list[i] = data[0].split(',')
        i = i + 1
    for data in data_list:
        data[0] = data[0].split(':')[1]
        data[-1] = data[-1].split(';')[0]
    for j in range(len(data_list)):
        for k in range(len(data_list[j])):
            data_list[j][k] = data_list[j][k].strip()


def findEntropyOutcome(attrName,attrIndex):
    global outcomeRes
    for data in data_list:
        outcomeRes.append(data[attrIndex])
    count = Counter(outcomeRes)
    yesCount = count['Yes']
    noCount = count['No']
    totalCount = len(outcomeRes)
    entropyOutcome = (((float(yesCount)/totalCount) * math.log((float(totalCount)/yesCount),2) + ((float(noCount)/totalCount)* math.log((float(totalCount)/noCount),2))))
    return entropyOutcome

    
def findEntropy(attrName, attrIndex):
    global entropy_list_attr
    temp_list_yes_no  = []
    temp_list_counter = []
    ase = []
    outcome = []
    for data in data_list:
        outcome.append(data[attrIndex])
    count = Counter(outcome)
    branchList = []
    for c in count:
        branchList.append(c)
        ase.append(c)
        ase.append([i for i, x in enumerate(outcome) if x == c])
    st = []
    totalCount = len(data_list)
    entropyOutcome = 0
    dict = {}
    for i in range(len(ase)):
        st.append([])
        if i % 2 == 0:
            dict.update({ase[i]:ase[i+1]})
            for j in ase[i+1]:
                st[i].append(outcomeRes[j])
            count2 = Counter(st[i])
            yesCount = count2['Yes']
            noCount = count2['No']
            probCount = yesCount + noCount
            temp_list_yes_no.append([yesCount,noCount,probCount])
            temp_list_counter.append(ase[i])
            i = i+1
            if noCount == 0 or yesCount == 0:
                continue
            else:
                entropyOutcome = float(entropyOutcome) + ((float(probCount)/totalCount)*(((float(yesCount)/probCount) * math.log((float(probCount)/yesCount),2) 
                                                                                      + ((float(noCount)/probCount)* math.log((float(probCount)/noCount),2)))))
    entropy_list_attr.update({attrName:([attrName,entropyOutcome, branchList, count, dict, temp_list_yes_no, data_list])})
    return entropyOutcome
                
class TreeNode(object):
    def __init__(self,nodeName, nodeType = None, data = None, attrDict =None, entropy = 0.0, branchList = None, upLink = None):
        self.name     = nodeName
        self.entropy  = entropy
        self.upLink   = upLink
        self.downLinks = []
        self.nodeType = nodeType
        self.visited = False
        if self.nodeType == 'A':  
            self.branchList = branchList
            self.attrChosen = attrDict.copy()
            self.data = data
            for branch in branchList:
                self.downLinks.append( TreeNode(nodeName = branch, upLink= self, nodeType = 'V' ) )

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
            tempNode = TreeNode(nodeName,'A', data, attrDict, entropy, branchList, upLink = None)
            self.rootNode = tempNode
            self.lastTraversedNode = tempNode
            return tempNode
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
                    tempNode =  TreeNode(nodeName, 'V', data, attrDict, entropy, branchList, upLink = valueNode)
                else:
                    tempNode =  TreeNode(nodeName, 'T', data, attrDict, entropy, branchList, upLink = valueNode)
                    valueNode.downLinks.append(tempNode)
                    valueNode.visited = True
            else:
                tempNode =  TreeNode(nodeName, 'A', data, attrDict, entropy, branchList, upLink = valueNode)
                valueNode.downLinks.append(tempNode)
                valueNode.visited = True
            self.lastTraversedNode = tempNode
            return tempNode
        
        if endOfPath == True:
            self.lastTraversedNode = self.goLevelUp(self.lastTraversedNode)    
        
    def goLevelUp(self, currentLevelNode):
        if currentLevelNode.upLink.nodeType == 'V':
            return currentLevelNode.upLink.upLink
        if currentLevelNode.upLink.nodeType == 'A':
            return currentLevelNode.upLink 
    
    def goLevelDown(self, currentLevelNode, branch):
        valueNode = None
        branchindex = 0
        downlinks = currentLevelNode.downLinks 
        for link in downlinks:
            if link.name == branch:
                index = branchindex
                break
            branchindex += 1
        if branchindex == len(downlinks):
            return None
        else:
            valueNode = downlinks[index]
        links = valueNode.downLinks
        return links[0]
         
        #
        #return valueNode
    def chooseAttributeNode(self,branchName):
        entropyDictAttr = {}
        entropy_list = []
        entropy_index_list = []
        attrdict = self.lastTraversedNode.attrChosen.copy()
        currententropy = self.lastTraversedNode.entropy
        currentdata = self.lastTraversedNode.data
        branchEntropy = currentdata[1]
        currRows = currentdata[4]
        outcome = []
        node_data_list = currentdata[6]
        data_list_local = []
        for i in currRows[branchName]:
            outcome.append(node_data_list[i][-1])
            data_list_local.append(node_data_list[i])
        if len(outcome) <= 1:
            return [branchName, outcome[0]]
        else:
            count = Counter(outcome)
            if len(count) == 1:
                terminalValue = count.keys()[0]
                return [branchName, terminalValue]
        attrdict = dict((k, v) for k, v in attrdict.iteritems() if v == False)
        if len(attrdict) == 0:
            return None
        for attr in attrdict:
                attrIndex = data_hdr_list.index(attr)
                entropy_index_list.append(attrIndex)
                entropy_list.append(self.calculateEntropy(attr,attrIndex, currentdata, branchName, entropyDictAttr, node_data_list, data_list_local))
        diffEntropy = []
        diffEntropy[:] = [currententropy-e for e in entropy_list]
        maxattr = diffEntropy.index(max(diffEntropy))
        finalAttr = data_hdr_list[entropy_index_list[maxattr]]
        return {finalAttr:entropyDictAttr[finalAttr]}
                
    def calculateEntropy(self,attr, attrIndex, currentdata,branchName, dictAttr, node_data_list, data_list_local):
        currRows = currentdata[4]
        outcome = []
        for i in currRows[branchName]:
            outcome.append(node_data_list[i][attrIndex])
        count = Counter(outcome)
        dict = {}
        countList = []
        branchList = []
        for c in count:
            branchList.append(c)
            dict.update({c:[i for i, x in enumerate(outcome) if x == c]})
            countList.append(c)
            countList.append([i for i, x in enumerate(outcome) if x == c])
        totalCount = len(outcome)
        st = []
        temp_list_yes_no  = []
        entropyOutcome = 0
        for i in range(len(countList)):
            st.append([])
            if i % 2 == 0:
                for j in countList[i+1]:
                    st[i].append(outcomeRes[j])
                count2 = Counter(st[i])
                yesCount = count2['Yes']
                noCount = count2['No']
                probCount = yesCount + noCount
                temp_list_yes_no.append([yesCount,noCount,probCount]) 
                i = i+1 
                if noCount == 0 or yesCount == 0:
                    continue
                else:
                    entropyOutcome = float(entropyOutcome) + ((float(probCount)/totalCount)*(((float(yesCount)/probCount) * math.log((float(probCount)/yesCount),2) 
                                                                              + ((float(noCount)/probCount)* math.log((float(probCount)/noCount),2)))))
        dictAttr.update({attr:([attr,entropyOutcome, branchList, count, dict, temp_list_yes_no, data_list_local])})     
        return entropyOutcome
        
    def traverseTree(self, currentNode = rootNode , level = 1): 
        resultList = []   
        if currentNode.nodeType != 'V':
            leveldata = "Level " + level + " - " + currentNode.name
            resultList.append(leveldata)
            print '(', currentNode.name, " -", currentNode.nodeType , " - Level - " , level, ' )' #" - Parent - ", currentNode.upLink.name,
        else:
            level = level - 1
        for children in currentNode.downLinks:
            self.traverseTree(children , level+1 )       

    def checkExitTree(self, currentNode = rootNode ):
        
        if currentNode.downLinks is None:
            if currentNode.nodeType == 'T':
                return True
            else:
                return False
        else:
            for children in currentNode.downLinks:
                return ( self.checkExitTree(children) and True) 
            
    def chooseNextBranch(self, currentLevelNode):
        valueNode = None
        downlinks = []
        downlinks = currentLevelNode.downLinks
        branchindex = 0 
        for link in downlinks:
            if link.visited == False:
                index = branchindex
                break
            branchindex += 1
        if branchindex == len(downlinks):
            return None
        else:
            return downlinks[index].name
    
    
    def predictResult(self, currentNode, predictionAttr):          
        print predictionAttr
        attrDict = []
        attrDict = dict((k, v) for k, v in predictionAttr.iteritems() if v[1] == False).copy()
        if len(attrDict) == 0:
            return "Incomplete Model"
        if currentNode.nodeType == 'T':
            return currentNode.name
        if currentNode.nodeType == 'A':
            if predictionAttr[currentNode.name]:
                branch = predictionAttr[currentNode.name][0]
                print branch
                predictionAttr.update({currentNode.name:[branch, True]})
                nextNode = self.goLevelDown(currentNode, branch)
                if nextNode == None:
                    return "Incomplete Model"
                currentNode = nextNode
            else:
                for children in currentNode.downLinks:
                    return self.predictResult(children, predictionAttr)
        return self.predictResult(currentNode , predictionAttr )       

readFile()
outcomeEntropyRes = 0
outcomeEntropyRes = findEntropyOutcome(data_hdr_list[-1],-1)
for i in range(len(data_hdr_list)-1):
    data_hdr_entropy.append([])
entropyList = []
for i in range(len(data_hdr_list)-1):
    entropyList.append(findEntropy(data_hdr_list[i],i))
diffEntropy = []
diffEntropy[:] = [outcomeEntropyRes-e for e in entropyList]
indexattr = diffEntropy.index(max(diffEntropy))

rootAttribute = data_hdr_list[indexattr]
root = Tree()
branchList = entropy_list_attr[rootAttribute][2]
root.addNode(rootAttribute,entropy_list_attr[rootAttribute],entropy_list_attr[rootAttribute][1], branchList)

current = root
treeIncomplete = True
while treeIncomplete:
    branch = current.chooseNextBranch(current.lastTraversedNode)
    if branch == None:
        if current.lastTraversedNode.upLink == None:
            treeInComplete = False
            break
        else:
            current.lastTraversedNode = current.goLevelUp(current.lastTraversedNode)
             #treeIncomplete = False # Tree complete
        continue
    attrData = current.chooseAttributeNode(branch)
    if attrData == None:
        continue
    if len(attrData) > 1:
        valueAttr = attrData[1]
        newNode = current.addNode(nodeName = valueAttr, whichBranch = branch, endOfPath = True)
        current.lastTraversedNode = current.goLevelUp(current.lastTraversedNode)
        continue
    attr = attrData.keys()[0]
    data = attrData[attr]
    branches = data[2]
    newNode = current.addNode(attr, data , data[1], branches, branch)
    if current.checkExitTree(current.lastTraversedNode):
        current.lastTraversedNode = current.goLevelUp(current.lastTraversedNode)

root.traverseTree(root.rootNode)
question = "Size = Large; Occupied = Moderate; Price = Cheap; Music = Loud; Location =City-Center; VIP = No; Favorite Beer = No"
qList = question.split(';')
print qList
dictQuestion = {}
for i in range(len(qList)):
    dictQuestion[qList[i].split('=')[0].strip()] = [qList[i].split('=')[1].strip(),False]

for d in dictQuestion:
    print d,  dictQuestion[d]
    
print root.predictResult(root.rootNode, dictQuestion)

