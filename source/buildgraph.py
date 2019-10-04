import numpy as np
import matplotlib.pyplot as plt
import glob, os
import scipy.constants as sc
import codecs
import unicodedata
import chardet



data = []
rausch = []
i = 0

for file in glob.glob("../../radiodata/raw/*.tim"):
	i += 1
	print('hi')
	if i == 1:
		print(file)

		print(chardet.detect(open(file,'rb').read()))
		'''
		with open(file) as f:
		    content = f.readlines()
		# you may also want to remove whitespace characters like \n at the end of each line
		content = [x.strip() for x in content] 
		'''

		#lines = codecs.open(file, 'r', encoding='hex').readlines()[1000:]

		#data = (np.genfromtxt(file,delimiter = '',skip_header = 100,encoding='latin-1'))
		#data = np.frombuffer(open(file).read().replace('\n','').decode('hex'), dtype=numpy.uint32, encoding='latin-1').byteswap()
		#print(str((file[-9:-4])))
		#print(file[0:-9])
		#rausch.append(np.genfromtxt(file[0:-9]+str(int(file[-9:-4])+1)+'.csv',delimiter = '',skip_header = 46))
		#print(file)
		#print(lines)
		#x = data[:,0]
		#y = np.sqrt(np.array(data[:,2])**2+np.array(data[:,3])**2)
		#y = data[:,1]
		
		#plt.plot(sc.c/x,y,label = file)#-y_r)
		#plt.legend(loc = 'best')
		
		#break
#plt.show()	
'''
#print(data)
print(data)
x = data[0][:,1]
y = np.sqrt(np.array(data[0][:,2])**2+np.array(data[0][:,3])**2)

#x_r = rausch[0][:,1]
#y_r = np.sqrt(np.array(rausch[0][:,2])**2+np.array(rausch[0][:,3])**2)

print('x:',x)
print('y:',y)

plt.figure()
plt.plot(x,y)#-y_r)
plt.show()
'''