import os
import linecache as lc
from EHS_compare import compare_func as com
'''
半成品
'''
n = int(input("how many lists of test data do you want"))
if(n <= 10):
    direction_name = input("你想打开哪天的数据（0405/0406/0407）")
    file_name = os.listdir(str(direction_name))
    print(file_name)
    path = str(direction_name)
    a = int(input("输入一个数据（数据决定了随机抽到的组，输入个大点的）："))
    path = path + os.sep
    for i in range(n):
        for file in file_name:
            with open(str(path+file),"r") as f:
                count = 0
                while True:
                    buffer = f.read(1024 * 8192)
                    if not buffer:
                        break
                    count += buffer.count('\n')
                f.close()
                #print(count)
                if(count == 0):continue          #跳过空文件
                aaa = a%count+1
                a = int(a*19/20)+500
                the_data = lc.getline(str(path+file),aaa)
                data = the_data.split()
                with open("output"+str(i),"a") as f:
                    f.write(str(data[0])+str(data[1])+"\t"+str(data[2])+\
                            str(data[3])+str(data[4])+"\t"+str(data[-1])+"\n")


