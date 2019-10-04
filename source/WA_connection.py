import numpy as np
import matplotlib.pyplot as plt
import glob, os
import scipy.constants as sc
import scipy.odr as sdr
import sys

jsol=0.06206206206206133
i1=396
i2=551

def gaussian_ba(b,x):
    return b[2]*np.exp(-(x-b[0])**2/(2*b[1]**2))+b[3]+b[4]*x
def gauss_fit_ba(datax,datay,errory,beta0=[0,1,1,0,0]):
    mod = sdr.Model(gaussian_ba)
    dat = sdr.RealData(datax,datay,sy=errory)
    odr = sdr.ODR(dat,mod,beta0=beta0)
    odr.set_job(fit_type=2)
    res = odr.run()
    return [res.beta,res.sd_beta,res.res_var]

data = []

data = np.genfromtxt("../../../../radiodata/raw/sto25_CYG_A_cont_83483.csv",delimiter = ',')
print(data)
print(data.shape)
x = data[:,3]
print(x)

def aver(l,i):
  return (l[i-1]+l[i]+l[i+1])/3

##mag 4 h sein
##dann 3 a?

anga=data[:,1]
angh=data[:,2]
# plt.plot(np.arange(len(anga)),anga)
# plt.axvline(i1)
# plt.axvline(i2)

# plt.show()
# sys.exit()
dda=aver(anga,i1)-aver(anga,i2)
ddh=aver(angh,i1)-aver(angh,i2)
print("dda",dda)
print("ddh",ddh)
dda*=(np.pi/180)
ddh*=(np.pi/180)


######
#y is normed by maximum !!
######
y = np.sqrt(data[:,6]**2+data[:,7]**2)/max(np.sqrt(data[:,6]**2+data[:,7]**2))

fit_x = np.linspace(19.8,20.2,1000)

sigmay=y*0.01*np.sqrt(0.44212332532648374)#chi corrected errors (added by simon)

fit = gauss_fit_ba(x,y,sigmay,[20,0.02,0.6,0.4,0.02])
relerr=(fit[1][1]/fit[0][1])
print(relerr)
# sys.exit()
fit_y = gaussian_ba(fit[0],x)

chi=0.0
for i in range(len(x)):
  chi+=((fit_y[i]-y[i])/sigmay[i])**2
chi/=len(x)-5
print(chi,fit[2])#abweichungen von perfekter chi korrektur erwartet und ignoriert

fwhm=fit[0][1]*2*np.sqrt(2*np.log(2))
print(fwhm)#alternative/deutlich genauerere methode das fwhm zu bestimmen, hat aber keine möglichkeit, min und max T zu bestimmen, daher eigentlich nur zum vergleich, aber da originale Version um ca 6 sigma abweicht....könnte man die punkte in resolution anpassen[leider hab ich keine ahnung wie du auf die zeiten gekommen bist/kann das nicht {alleine] machen/bräuchte neue Zeiten], alternativ müssten die Fehler größer werden (deutlich), wobei hier beides unser ergebnis besser machen würde [wenn auch kleinere Fehler wohl zu bevorzugen sind]








a1=(72+(16+(24.5)/60)/60)*(np.pi/180)
a2=(72+(47+(38.3)/60)/60)*(np.pi/180)
h1=(41+(5+(33.5)/60)/60)*(np.pi/180)
h2=(41+(36+(49.5)/60)/60)*(np.pi/180)



da=abs(a2-a1)
dh=abs(h2-h1)
print("da",da*(180/np.pi))
print("dh",dh*(180/np.pi))


da-=dda
dh-=ddh
a1+=dda/2
a2-=dda/2
h1+=ddh/2
h2-=ddh/2




meanh=(h1+h2)/2
d=np.sqrt(dh**2+(np.cos(meanh)*da)**2)#näherung nur für fehler benutzt
d=np.arccos(np.cos(h1)*np.cos(h2)*np.cos(a1-a2)+np.sin(h1)*np.sin(h2))#hier andere näherung...dda symmetrisch um ai
d*=180/np.pi
d*=fwhm/jsol
sigmad=relerr*d
print("measure::",d,"+-",sigmad)


lamda=0.211061140542#in m#0.217941#
durchmesser=25.0 #in m
theory=1.22*(lamda/durchmesser)*(180/np.pi)
sigmad=np.sqrt(1/12+(theory*(1-np.cos(0.05*(np.pi/180))))**2)#added schiefe fehler (wenn auch sinnlos af)

sigmatheory=(sigmad/durchmesser)*theory
print("theorie::",theory,"+-",sigmatheory)


print("binnkorr",d*((0+(0+(0.1)/60)/60)*(np.pi/180))/h1)#folglich völlig egal

#ja wir haben literally kleinere Fehler als der Theoriewert, daher...hier der wirkliche radius

realdurchmesser=durchmesser*(theory/d)
realdurchmessersigma=relerr*realdurchmesser
print("realer durchmesser [m]:",realdurchmesser,"+-",realdurchmessersigma)

wink=np.arccos(realdurchmesser/durchmesser)*(180/np.pi)
print("this would be the result of a angular error of",wink)

