import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

filename = os.listdir("src")
print(filename)
filename = os.listdir("src")
path = "src"
data = {}
path = path+os.sep
for file in filename:
    with open(path+file) as f:
        gap = 0
        for line in f:
            list = line.split()
            gap += abs(float(list[-1])-float(list[-2]))
        data[int(file[:-10])] = gap


data2 = sorted(data.items(),key=lambda x:x[0])

x = []
y = []
for z in data2:
    x.append(z[0])
for v in data2:
    y.append(100-v[1])



color=['r',]

X = np.asarray(x)
Y = np.asarray(y)

plt.title = ("Accuracy of Simulation Times")
plt.figure(dpi=100)
l = plt.axline(xy1=(0,100),slope=0,linewidth=1,color='b')
c=[0,max(x),min(y),max(y)]
plt.axis(c)
plt.grid()
plt.ylim(c[2],c[-1])
plt.xlabel("ST")
plt.ylabel('Acc')
p = zip(X,Y)

plt.plot(X,Y)

sns.set_style("dark")


for X,Y in p:
    plt.text(X,Y,(X,(Y)%99/10),ha='center',c="grey",fontsize='10')


plt.show()




