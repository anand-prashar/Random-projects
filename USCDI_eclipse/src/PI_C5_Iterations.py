'''
Created on Jul 21, 2016

@author: anand
'''

def whileLoop():
    i = 0;
    while i <=500:
        
        i+=1
        if i == 2:
            continue; #remain in loop
        elif i == 5:
            break;    # exit loop before reaching 500
        
        print i  

def forLoop():
    
    # list is created Before loop
    myList  = {'Anand','Ravi','Shashi'}
    for nameVar in myList:
        print nameVar
    
    #list is created during loop itself
    sumVal = 0
    for value in {1,2,3,4,5}:
        sumVal+=value
    print '\n\nsum=', str(sumVal) 

# Notice use of NONE keyword
def maxMin():
    
    maxVal = None
    print 'Type of' ,maxVal, 'variable : ', type(maxVal);
    
    minVal = None
    for value in {10,2,3,40,5}:
        
        if (minVal>value) or (minVal is None) :
            minVal = value
        
        if (maxVal<value) or (maxVal is None) :
            maxVal = value    
            
    print 'Max Value =',maxVal, '\nMin Value =',minVal;        

    

#-----------------------------------------------------------------------------
#whileLoop();

#forLoop();


maxMin();