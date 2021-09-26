"""
第二层封装
"""
from EHS_compare import compare_func as com
import random
import time

def random_sample(time2):
    '''
    3.29添加
    :param time1: 起牌次数
    :param time2: 测试次数（对于每次起牌而言）
    :return:输出至time2_static.txt
    '''
    cards = [_ for _ in range(52)]


    filename = str(time2) + 'static.txt'   # 建立测试文本文档
    with open(filename, 'w') as f:
        with open("output/output1", 'r') as dt:
            for lines in dt:
                datalist = lines.split()
                out_cards = datalist[0]
                out_cards111 = out_cards[1:-1]
                out_cards222 = out_cards111.split(",")
                our_cards = [int(out_cards222[0]),int(out_cards222[1])]  #很笨，但有效
                pub = datalist[1]
                pub1 = pub[1:-1].split(",")
                public_cards = [int(pub1[0]),int(pub1[1]),int(pub1[2])]
                cards2 = [_ for _ in range(52) ]
                for x in public_cards:
                    cards2.remove(x)
                for y in our_cards:
                    cards2.remove(y)
                     # win rp计算(抽样胜率)
                win_rp = 0
                for j in range(time2):
                    other_cards = random.sample(cards2, 4)
                    two_pub_cards = other_cards[0:2]
                    opp_cards = other_cards[2:4]
                    judge = com.Judgement(our_cards,opp_cards,public_cards+two_pub_cards)
                    if judge.status == 0:
                        win_rp += 1
                    elif judge.status == 1:
                        win_rp += 0.5

                f.write(str(our_cards)+'\t')
                f.write(str(public_cards)+'\t')
                f.write(str(win_rp/time2)+'\t')
                f.write(datalist[-1]+'\n')







if __name__ == "__main__":
    x = [52, 100, 1000, 5000, 7500, 10000, 30000, 50000, 100000, 500000]
    for _ in x:
        start = time.perf_counter()
        random_sample(_)
        end = time.perf_counter()
        print(str(_)+": "+str(end-start)+" s")


