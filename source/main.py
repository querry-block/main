# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 12:58:18 2019

@author: Marcel
"""

import numpy as np
import matplotlib.pyplot as plt
from WA_connection import *
import graph_api as ga

class I1D():
    N = 0
    N_sample = 0
    T = 0
    beta = 0
    latice = None
    U = 0
    U_theo = None
    count = 0
    
    def get_latice(self):
        return self.latice
    def calc_U_theo(self):
        self.U_theo = -(self.N-1)/self.N*np.tanh(self.beta)
    def init(self,N,N_sample,T):
        self.N = N
        self.N_sample = N_sample
        self.T = T
        self.beta = 1.0/T
        self.latice = np.random.choice([-0.5,0.5],N)
        self.calc_U_theo()
        
    def Energy(self):
        void = np.zeros(1)
        s1 = np.append(void,self.latice)
        s2 = np.append(self.latice,void)
        return -np.sum(s1*s2)
    def MCC_step(self):
        E = self.Energy()
        r = np.random.uniform()
        j = round(r*self.N-1) # kein +1 da Spins von 0 bis N-1 durchnummerriert sind             
        self.latice[j] = -self.latice[j]
        E_prime = self.Energy()-E
        q = np.exp(-self.beta*E_prime)
        r_n = np.random.uniform()
        if q < r_n:
            self.count += 1
            self.latice[j] = -self.latice[j] #zurückflippen wenn der flipp nicht akzeptiert wird
    def run(self):
        E_list = []
        N_wait = int(self.N_sample/10)
        for i in range(N_wait):
            self.MCC_step()
        for i in range(self.N_sample):
            self.MCC_step()
            self.U += self.Energy()
            E_list += [self.Energy()]
        self.U = self.U/self.N/self.N_sample
        return self.U,self.U_theo,E_list



a = I1D()
a.init(10,1000000,4) 
U, U_theo, E_list = a.run()
print(U,U_theo)
#fig1, ax1 = plt.subplots(1,1,figsize=(16,9))
#ax1.plot(E_list)


     