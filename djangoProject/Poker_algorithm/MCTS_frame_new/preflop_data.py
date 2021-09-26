'''
7.6
preflop_data是对ultimate table的处理
实现功能为从13*13的数据中直接读取出52*52的表格（根据映射的数学关系
同样实现了直接读取数据降低复杂度的功能
'''

def get_13table():
    file_name = "preflop_table_ultimate.txt"
    with open(file_name,"r")as f:
        preflop_table = [[]]*13
        line = f.readline()
        i = 0
        while line:
            line = line.strip('\n')
            line = line.split()
            line = list(map(int, line))
            preflop_table[i] = line
            i += 1
            line = f.readline()


    #for i in range(52):
     #   print(preflop_table[i])
    return  preflop_table

def get_table():
    # 52*52空表
    file_name = "preflop_table_ultimate.txt"
    table = [[0] * 52 for m in range(52)]
    try:
        with open(file_name, "r")as f:
            preflop_table = [[]] * 13

            line = f.readline()
            k = 0
            while line:
                line = line.strip('\n')
                line = line.split()
                line = list(map(int, line))
                preflop_table[k] = line
                k += 1
                line = f.readline()
    except FileNotFoundError:
        file_name = "Poker_algorithm/MCTS_frame_new/preflop_table_ultimate.txt"
        with open(file_name, "r")as f:
            preflop_table = [[]] * 13

            line = f.readline()
            k = 0
            while line:
                line = line.strip('\n')
                line = line.split()
                line = list(map(int, line))
                preflop_table[k] = line
                k += 1
                line = f.readline()

    for i in range(52):
        for j in range(52):

            if i==j:
                table[i][j]=0
            elif (i%4)==(j%4):
                a = int(i/4)
                b = int(j/4)
                if a>b:
                    table[i][j] = preflop_table[b][a]
                else:
                    table[i][j] = preflop_table[a][b]
            else:
                a = int(i/4)
                b = int(j/4)

                if a>b:
                    table[i][j] = preflop_table[a][b]
                else:
                    table[i][j] = preflop_table[b][a]


    return table


if __name__ == '__main__':
    prefloptable = get_table()
    set = [0]*31
    for i in range(51):
        for j in range(i+1, 52):
            x = prefloptable[i][j]
            p = int ((x - 650)/5)
            if p >= 30:
                p = 30
            set[p]+=1
    q = sum(set)
    print(set)
    print(q)
    for i in range(31):
        set[i] /= q
        if i > 0:
            set[i] += set[i-1]
    print(set)
