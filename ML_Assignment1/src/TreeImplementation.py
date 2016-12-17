'''
Created on Sep 14, 2016

@author: anand
'''
data_hdr_list = ['Size','Occupied','Music'] 
class TreeNode(object):

    name = 'Default'
    entropy = 0.0
    branchList = []
    nodeType = None # 'A' - for attribute  ;  'V' - value/branch node
    downLinks = []
    upLink = None
    visited = None
    attrChosen = {}
    data = []
    def __init__(self,nodeName, data = None, attrDict =None, entropy = 0.0, branchList = None, upLink = None):
        self.name     = nodeName
        self.entropy  = entropy
        self.upLink   = upLink
         
        if branchList is None:
            self.nodeType = 'V'
        else:
            self.nodeType = 'A'
            self.attrChosen = attrDict.copy()
            self.data = data
            for branch in branchList:
                self.downLinks.append( TreeNode(nodeName = branch, upLink= self ) )
                
        

class Tree(object):
    
    rootNode = None
    lastTraversedNode = None
    tempNode = None
    
    def addNode(self, nodeName = None,data = None, entropy = None, branchList = None, whichBranch = None, endOfPath = None):
        
        attrDict = {}
        if self.rootNode is None:
            for attrName in data_hdr_list:
                attrDict.update({attrName:False})
            attrDict.update({nodeName:True})
            tempNode = TreeNode(nodeName, data, attrDict, entropy, branchList, upLink = None)
            self.rootNode = tempNode
            self.lastTraversedNode = tempNode
        else:
            valueNode = None
            downlinks = self.lastTraversedNode.downLinks 
            if downlinks:
                index = downlinks.index(whichBranch)
                valueNode = self.lastTraversedNode.downLinks[index]  # ?
            attrDict = self.goLevelUp(self.lastTraversedNode).attrChosen.copy()
            attrDict.update({nodeName:True})
            tempNode =  TreeNode(nodeName, data, attrDict, entropy, branchList, upLink = valueNode )
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
        if currentLevelNode.upLink.nodeType == 'A':
            return currentLevelNode.upLink.upLink
        if currentLevelNode.upLink.nodeType == 'V':
            return currentLevelNode.upLink 
           
        