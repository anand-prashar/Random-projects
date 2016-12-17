
def  useThisforSmallFile():

	#print 'Use read()  method when you know data is going to be small in the file'

	fHandle = open('data_file.txt','r')
	#print fHandle
	fData = fHandle.read()
	print '\n\nFile Data = \n', fData
	
	fHandle.close();


def useThisforLargerFile():
	
	fHandle2 = open('data_file.txt')
	
	for tempStr in fHandle2:
		print tempStr

def writeIntoFile():
	
	fHandle3 = open('data_file_Write.txt','w')
	
	fHandle3.write('lINE 1 entered in new file\n')
	fHandle3.write('lINE 2 ENTERED.')	
	fHandle3.close();



#useThisforSmallFile()  
useThisforLargerFile()
writeIntoFile()  