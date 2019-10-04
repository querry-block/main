import numpy as np
import matplotlib.pyplot as plt
import glob, os
import scipy.constants as sc
import scipy.odr as sdr

bincom=25
poimode=False

def gaussian_ba(b,x):
    return b[2]*np.exp(-(x-b[0])**2/2/(b[1]**2))+b[3]
def gauss_fit_ba(datax,datay,errory,beta0=[0,1,1,0]):
    mod = sdr.Model(gaussian_ba)
    dat = sdr.RealData(datax,datay,sy=errory)
    odr = sdr.ODR(dat,mod,beta0=beta0)
    odr.set_job(fit_type=2)
    res = odr.run()
    return [res.beta,res.sd_beta,res.res_var]

data = []

data = np.genfromtxt("../../../../radiodata/raw/sto25_CYG_A_cont_83483.csv",delimiter = ',')

x = data[:,3]

######
#y is normed by maximum !!
######
y = np.sqrt(data[:,6]**2+data[:,7]**2)/max(np.sqrt(data[:,6]**2+data[:,7]**2))

fit_x = np.linspace(19.8,20.2,1000)


sigmay=y*0.01*np.sqrt(0.44212332532648374)#chi corrected errors (added by simon)
fit = gauss_fit_ba(x,y,sigmay,[20,0.02,0.6,0.4])
fit_y = gaussian_ba(fit[0],fit_x)
half_max = (max(fit_y)/2+min(fit_y)/2)


def combinebins(x):
  if bincom==1:return x
  ret=[]
  ac=[]
  for i in range(len(x)):
    ac.append(x[i])
    if (i+1)%bincom==0:
      ret.append(np.mean(ac))
      ac=[]
  
  
  return np.array(ret)

print(fit)
plt.figure()

a=combinebins(x-fit[0][0])
b=-a
ya=combinebins(y)
yb=combinebins(y*1)
if poimode:
  plt.plot(a,ya, ls = '', marker = '.',label="original")
  plt.plot(b,yb, ls = '', marker = '.',label="negate")
else:
  plt.plot(a,ya,label="original")
  plt.plot(b,yb,label="negate")

plt.legend()
plt.show()
