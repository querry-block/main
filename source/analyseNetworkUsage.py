#angle calibration max style


import matplotlib.pyplot as plt
import numpy as np

#disply my raw data:
    
import csv
from datetime import datetime

filepath="C:/Users/User/source/radiodata/raw/sto25_CYG_A_cont_83483.csv"

def read(filepath):
    row=[]
    stringDate=[]
    with open(filepath, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for line in spamreader:#2012-12-02
            datum=datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
            row.append([float(datum.second+60*datum.minute),float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),np.sqrt(float(line[6])**2+float(line[7])**2)])
            stringDate.append(line[0])
    row=np.array(row)
    return{"timeString":stringDate,"time":row[:,0],"hourangle":row[:,0]/86400*360,"azimuth":row[:,1],"altitude":row[:,2],"ascension":row[:,3],"declination":row[:,4],"phase":row[:,5],"intensity":row[:,6]/max(row[:,6])}
    '''
    timeString->string
    time->relative seconds
    houranngle->in degree
    azimuth->degree
    altitude->degree
    ascension->degree
    declination->degree
    phase->?
    intensity->arbitrary units
    '''
    
        
          
data=read(filepath)
#%%
#raw data
plt.figure()
plt.title("angle calibration")
plt.xlabel("hourangle in degree")
plt.ylabel("intensity in arb.Units")
plt.plot(data["hourangle"],data["intensity"],label="raw data")
plt.legend()

#what julian and simon look at
# plt.figure()
# plt.title("angle calibration simon style")
# plt.xlabel("local ascension in degree")
# plt.ylabel("intensity in arb.Units")
# plt.plot(data["ascension"],data["intensity"],label="raw data")
# plt.legend()


#%%
#fitting a curve onto the data inspired by simons and julians code

import scipy.odr as sdr

def gaussian(b,x):
    return b[0]/np.sqrt(2*np.pi*b[2]**2)*np.exp(-(x-b[1])**2/(2*b[2]**2))+b[3]+b[4]*x
    """
    b[0]->scale
    b[1]->mean
    b[2]->variance
    b[3]->y-shift
    b[4]->superimposed linear function
    """
def gauss_fit(datax,datay,errory,beta0=[0,1,1,0,0]):
    mod = sdr.Model(gaussian)
    dat = sdr.RealData(datax,datay,sy=errory)
    odr = sdr.ODR(dat,mod,beta0=beta0)
    odr.set_job(fit_type=2)
    res = odr.run()
    return res
    #return [res.beta,res.sd_beta,res.res_var]

sigma=data["intensity"]*0.01#should be proportional to the data
plt.title("fitfunction and actual data")
plt.xlabel("hourangle in degree")
plt.ylabel("intensity in arb.Units")
plt.errorbar(data["hourangle"],data["intensity"],sigma)
plt.plot(data["hourangle"],gaussian([1,10,0.5,0.3,0.01],data["hourangle"]))
plt.legend()

#%%

#fitting
fit = gauss_fit(data["hourangle"],data["intensity"],sigma,[1,10,0.5,0.3,0.01])
fit.pprint()
plt.title("fitfunction after fit and actual data")
plt.xlabel("hourangle in degree")
plt.ylabel("intensity in arb.Units")
plt.errorbar(data["hourangle"],data["intensity"],sigma,label="measurement")
plt.plot(data["hourangle"],gaussian(fit.beta,data["hourangle"]),label="fit")


#neatly show the results
print("Mean=%f +-%f degree" %(fit.beta[1],fit.sd_beta[1]))
print("Variance=%f+-%f degree"%(fit.beta[2],fit.sd_beta[2]))
halfWidth=2*np.sqrt(2*np.log(2))*fit.beta[2]
halfWidthError=2*np.sqrt(2*np.log(2))*fit.sd_beta[2]
print("Half width=%f+-%f degree"%(halfWidth,halfWidthError))
                     

#draw a vertical line at the half widths
halfWidthPosA=fit.beta[1]+halfWidth/2
halfWidthPosB=fit.beta[1]-halfWidth/2
plt.vlines(halfWidthPosA,0.4,1,label="half Width=%f+-%f"%(halfWidthPosA,halfWidthError/2))
plt.vlines(halfWidthPosB,0.4,1,label="half Width=%f+-%f"%(halfWidthPosB,halfWidthError/2))
plt.legend()
plt.savefig("fitfunctionAndData.pdf")
plt.show()

#%%
#find the error of the wind:
    #difference in azimuth between half width#the dish is shaking around
import statistics as stat

plt.figure()
plt.title("pointing direction of dish during measurement")
plt.xlabel("hourangle in degree")
plt.ylabel("local azimuth in degree")
plt.plot(data["hourangle"],data["azimuth"],label="position of dish")#the clipping was deduced->area inside half width
plt.vlines(halfWidthPosA,81.95,82.25,label="half Width=%f+-%f"%(halfWidthPosA,halfWidthError/2))
plt.vlines(halfWidthPosB,81.95,82.25,label="half Width=%f+-%f"%(halfWidthPosB,halfWidthError/2))

#to what position do these half width corespond to?->read it of: it is [455:667]

#fitting a line through the interval between the half widths
def line(b,x):
    return b[0]+b[1]*x

def line_fit(datax,datay,errory,beta0=[90,1]):
    mod = sdr.Model(line)
    dat = sdr.RealData(datax,datay,errory)
    odr = sdr.ODR(dat,mod,beta0=beta0)
    odr.set_job(fit_type=2)
    res = odr.run()
    return res

res=line_fit(data["hourangle"][455:667],data["azimuth"][455:667],0.4)
fitData=line(res.beta,data["hourangle"])
plt.plot(data["hourangle"],fitData,label="fit")
plt.legend()
plt.show()
#plt.savefig("errorWind.pdf")
res.pprint()

#print what the difference inbetween the fitted position of the dish corresponds to
print("angular difference of the dish(moved by wind)=%f"%(fitData[455]-fitData[667]))

#what is the error?
stat.pstdev(fitData-data["azimuth"])
#

#%%
