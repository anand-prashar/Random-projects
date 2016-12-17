'''
Created on Jul 21, 2016

@author: anand
'''
from string import upper
def accessStringByIndex():
    
    userString = 'AaBbCcDdEeFfGg';
    # --- using while loop
    i=0
    while i<len(userString):
        if i%2 != 0:
            print userString[i]
        i+=1

    # --- using for loop
    print('\n\nNow by interesting loop :')
    for someVariable in userString:
        if ord(someVariable) < 97:  # less than a's ASCII
            print someVariable
        
        
def subString():  # slicing
    
    ###  Does not include ending character in substring
    
    userString = 'Hello, This is Anand'
    anotherString = userString[7:11]   # <-------- slicing
    print anotherString
      
    #Notice Below !
    print userString[:5]
    print userString[15:]

def stringsAreImmutable():
    
    userString = 'Hello, This is Anand'
    userString[0] = 'h'

def appendStrings():
    
    userString = 'Hello, This is Anand'
    userString = userString[15:] + '-appends- Prashar'
    print userString          
    
    
def inOperator():
    
    userString = 'Hello, This is Anand'
    print 'X' in userString
    print 'H' in userString
    
    print '\ndone'
    
def listAllMethods_forAnyObject():
    
    myStr = '  dummy string dumma   '
    print dir(myStr)  # dir method - shows ALLL methods available for an object
    
    print  upper(myStr);  # way 1
    print myStr.upper();  # way 2
    
    print myStr.find('umm');
    print myStr.find('umm',10)  # can also specify where to start
    
    
    print 'remove whitespaces on both sides:', myStr.strip();  
    
    
       
#--------------------------------------------------------------------
#accessStringByIndex();        
#subString();
#stringsAreImmutable();
#appendStrings();
#inOperator();

def parseString_clipping():
    #Question : Extract email + domain
    
    data = 'From stephen.marquard@uct.ac.za Sat Jan 5 09:14:16 2008'
    startIndex = data.find('@');
    endIndex   = data.find(' ',startIndex);
    revIndex   = data.rfind(' ',0,startIndex); 
    print data[startIndex:endIndex]
    print data[revIndex+1:endIndex]
    

#listAllMethods_forAnyObject();
parseString_clipping();