import numpy as np
from random import gauss
import matplotlib.pyplot as plt


##kurzes skript um einen Wert in ein sigma umzurechnen...ein abstand von a resultiert in etwa a/ausgabe (a/0.7978239) als fehler....offensichtlich erhöht ein größeres N die genauigkeit dieser Zahl, aber ich denke mal auch schon 0.8 wäre gut genug



N=10000000

x=[]
for i in range(N):
  x.append(gauss(0, 1))

x=np.array(x)
x=np.abs(x)

print(np.mean(x))
# print(np.std(x))

# plt.hist(x)
# plt.show()