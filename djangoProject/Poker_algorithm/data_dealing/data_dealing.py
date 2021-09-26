'''
非常笨拙的数据处理
0405
'''
filename = [0]*10
for n in range(10):
    print(n)
    filename[n] = "data"+str(n)+".txt"
    print(filename[n])

with open("0409/testdata_ppot0409.txt", "r") as data:
    d=[]*10
    with open (filename[0],"w") as d0,open (filename[1],"w") as d1,open (filename[2],"w") as d2,open (filename[3],"w") as d3,\
    open (filename[4],"w") as d4,open (filename[5],"w") as d5,open (filename[6],"w") as d6,open (filename[7],"w") as d7,\
    open (filename[8],"w") as d8,open (filename[9],"w") as d9, open("0407/unexpected.txt", "w") as unx:
        for line in data:
            datalist = line.split()
            winp = int(float(datalist[-1])*10)
            if not (winp - 0):
                d0.write(line)
            elif not (winp - 1):
                d1.write(line)
            elif not (winp - 2):
                d2.write(line)
            elif not (winp - 3):
                d3.write(line)
            elif not (winp - 4):
                d4.write(line)
            elif not (winp - 5):
                d5.write(line)
            elif not (winp - 6):
                d6.write(line)
            elif not (winp - 7):
                d7.write(line)
            elif not (winp - 8):
                d8.write(line)
            elif not (winp - 9):
                d9.write(line)
            else:
                unx.write(line)
