import numpy as np
import matplotlib.pyplot as plt
import glob, os
import scipy.constants as sc
import scipy.odr as sdr


def gaussian_ba(b,x):
    return b[2]*np.exp(-(x-b[0])**2/2/(b[1]**2))+b[3]+b[4]*x
def gauss_fit_ba(datax,datay,errory,beta0=[0,1,1,0,0]):
    mod = sdr.Model(gaussian_ba)
    dat = sdr.RealData(datax,datay,sy=errory)
    odr = sdr.ODR(dat,mod,beta0=beta0)
    odr.set_job(fit_type=2)
    res = odr.run()
    return [res.beta,res.sd_beta,res.res_var]

data = []
rausch = []
i = 0
#plt.figure()

rausch = np.genfromtxt("../../radiodata/raw/sto25_CYG_A_cont_83483.csv",delimiter = ',')

x = rausch[:,3]
y = np.sqrt(rausch[:,6]**2+rausch[:,7]**2)/max(np.sqrt(rausch[:,6]**2+rausch[:,7]**2))

fit_x = np.linspace(19.8,20.2,1000)

fit = gauss_fit_ba(x,y,y*0.01,[20,0.02,0.6,0.4,0.02])
fit_y = gaussian_ba(fit[0],fit_x)
half_max = (max(fit_y)/2+min(fit_y)/2)
#fit_y.index(half_max)
#print([i for i, e in enumerate(fit_y) if e == half_max])
#print(np.argsort(abs(fit_y-half_max)))
print(fit)
plt.figure()
plt.title('fit_parameter = {}'.format(fit))
plt.plot(x,y, ls = '', marker = '.')
plt.plot(fit_x,fit_y)#,label	= 'fit_parameter = {}'.format(fit))
plt.axhline(half_max)
plt.axvline(fit_x[551],ls='-.', color = 'r', label = r'$\Delta x = {}$'.format(fit_x[551]-fit_x[396]))
plt.axvline(fit_x[396],ls='-.', color = 'r')
plt.legend(loc = 'best')

plt.figure()
plt.errorbar(x,gaussian_ba(fit[0],x)-y,yerr=0.01*y
,marker='.',ls='',color='b',label='$\chi^2/\mathrm{ndf}='+str(np.round(fit[2],5))+'$')
#plt.title('Residuen '+str(material[i]),fontsize=18)
plt.axhline(0,color='r',ls='--')
#plt.xlabel('energies in keV',fontsize=18)
#plt.ylabel('counts',fontsize=18)
plt.legend(loc='best', fontsize=15)

#plt.plot(rausch[:,6]/max(rausch[:,6]))
#plt.plot(rausch[:,7]/max(rausch[:,7]))

plt.show()
#print(rausch[:,6])


'''
for file in glob.glob("../../radiodata/raw/sto25_CYG_A_spec_83485.csv"):
	if i <= 5:
		print(file)
		data = (np.genfromtxt(file,delimiter = '',skip_header = 46))
		#print(str((file[-9:-4])))
		#print(file[0:-9])
		#rausch.append(np.genfromtxt(file[0:-9]+str(int(file[-9:-4])+1)+'.csv',delimiter = '',skip_header = 46))
		#print(file)
		x = data[:,1]
		y = np.sqrt(np.array(data[:,2])**2+np.array(data[:,3])**2)
	i += 1
	
	plt.plot(sc.c/x,y,label = file)#-y_r)
	plt.legend(loc = 'best')
		
		#break
plt.show()	
'''
#print(data)
''' 
print(data)
x = data[0][:,1]
y = np.sqrt(np.array(data[0][:,2])**2+np.array(data[0][:,3])**2)

#x_r = rausch[0][:,1]
#y_r = np.sqrt(np.array(rausch[0][:,2])**2+np.array(rausch[0][:,3])**2)

print('x:',x)
print('y:',y)

plt.figure()
plt.plot(sc.c/x,y)#-y_r)
plt.show()
'''