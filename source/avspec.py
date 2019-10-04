import csv
from datetime import datetime
import matplotlib.pyplot as plt
import sys
import numpy as np
import math

hi=1420405752
c=299792

pat="../../../../radiodata/raw/"
out="../../output/"

def read(filepath):
  ret=[]
  with open(filepath, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:#2012-12-02
      if len(row)!=7:continue
      
      ret.append({"channel":int(row[0]),"f":float(row[1]),"intensity1":float(row[2]),"intensity2":float(row[3]),"intensityC1":float(row[4]),"intensityC2":float(row[5]),"I":float(row[6])})
  return ret
def readN(n):
  # return read(pat+'sto25_CYG_A_spec_'+str(n)+'.csv')
  return read(pat+'sto25_CYG_A_spec_'+str(n)+'.csv')
aa=readN("83486")
def filter(a):
  y=[]
  x=[]
  for e in a:
    y.append(e["I"])
    x.append(e["f"])
  return x,y
x,y=filter(aa)

x=np.array(x)
y=np.array(y)


# rawmean=100000*c/np.mean(x)
# print(rawmean)

mean=np.sum(y*x)/np.sum(y)
mean=100000*c/mean
print(mean)




print(100000*c/np.min(x),100000*c/np.max(x))


plt.plot(x,y)
plt.show()