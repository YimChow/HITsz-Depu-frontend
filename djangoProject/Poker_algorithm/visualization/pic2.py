import numpy as np
import matplotlib.pyplot as plt


x=[52,100,1000,5000,7500,10000,30000,50000,100000,500000]

k = []
with open("time.txt") as f2:
    for line in f2:
        list = line.split(':')
        k.append(float(list[-1]))

c=[0,max(x),min(k),max(k)]

X = np.asarray(x)
Y = np.asarray(k)

plt.title = ("Accuracy of Simulation Times")
plt.figure(dpi=100)
l = plt.axline(xy1=(0,100),slope=0,linewidth=1,color='b')
c=[0,max(x),min(k),max(k)]
plt.axis(c)
plt.grid()
plt.ylim(c[2],c[-1])
plt.xlabel("ST")
plt.ylabel('Acc')
p = zip(X,Y)

plt.plot(X,Y)
for X,Y in p:
    plt.text(X,Y,(X,Y),ha='center',c="grey",fontsize='10')

plt.show()

