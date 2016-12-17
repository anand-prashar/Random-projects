'''
Created on Jul 17, 2016

@author: anand
'''
import random
#from math import ceil, floor

def calculator():
    try:
        a = int(input('Enter 1st number : '));
        b = int(input('Enter 2nd number : '));
    except:
        print '\nOnly numbers expected as operands\n';
        return;
        
    c = str(raw_input('Enter operator : '));
 
    if   c == '+':  result = a+b;
    elif c == "-":  result = a-b;
    elif c == '*':  result = a*b;
    elif c == '/':  result = a/b;
    elif c == '**': result = a**b;
    elif c == '%':  result = a%b;
    else         :  result = 'Unknown. Invalid operator';
    
    print('Result = '+ str(result));
    
def comparison_operator():
    a = 257;
    b = 257;
    c = 'immutable';
    d = 'immutable';
    
    #  on Integers
    print 'Integers:';
    print id(a), id(b);   # WHY ????? why are both variables stored at same place
    print a == b;
    print a is b;

    #  on Strings
    print '\nStrings:'
    print c == d;
    print c is d;    

def test():
    #result = input("enter a math expression : "); 
    #print result;
    print max(2,31,5);
    
def exercise1():
    try:
        workedHours = float(raw_input('Enter employee hours: '));    
        assert workedHours >= 0;
        workedRate = float(raw_input('Enter hourly rate: '));    
        assert workedRate >= 0;
    except:
        print 'Invalid Input';
        return;
    if  workedHours<=40: 
        amountPaid =  workedHours*workedRate;
    else:
        amountPaid =  40*workedRate + (workedHours-40)*workedRate*1.5;
        
    print 'Amount paid = ', str(amountPaid);        

#===============================================================================
# print('CALCULATOR\n');
# while True:
#     calculator(); 
#===============================================================================
   
#comparison_operator();   

def randomize():
    #===========================================================================
    # for i in range(10):
    #     x = int(floor(random.random()*100));
    #     print x;    
    #===========================================================================
    t = [1,5,2];
    print random.choice(t);


#test();    
#exercise1();

comparison_operator();
#randomize();
#print type(calculator);