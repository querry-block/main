import numpy as np
import matplotlib.pyplot as plt
import glob, os
import scipy.constants as sc
import scipy.odr as sdr


def gaussian_ba(b,x):
    return b[2]*np.exp(-(x-b[0])**2/2/(b[1]**2))+b[3]+b[4]*x
def gaussian_ba_simple(b,x):
    return gaussian_ba(b,x)-b[4]*(x-np.min(x))
def gaussian_ba_line(b,x):
    return b[4]*x
def gauss_fit_ba(datax,datay,errory,beta0=[0,1,1,0,0]):
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
fit = gauss_fit_ba(x,y,sigmay,[20,0.02,0.6,0.4,0.02])
fit_y = gaussian_ba(fit[0],fit_x)
half_max = (max(fit_y)/2+min(fit_y)/2)

fit_g= gaussian_ba_simple(fit[0],fit_x)
fit_l= gaussian_ba_line(fit[0],fit_x)

print(fit)
# plt.plot(np.arange(len(y)),y, ls = '', marker = '.')
plt.plot(fit_x,fit_y,label="fit")#,label	= 'fit_parameter = {}'.format(fit))
plt.plot(fit_x,fit_g,label="simple")#,label	= 'fit_parameter = {}'.format(fit))
plt.plot(fit_x,fit_l,label="line")#,label	= 'fit_parameter = {}'.format(fit))

plt.legend()
plt.show()
