
from EHS_compare import compare_func as com
from EHS_compare import HandStrength as HS
import random
import time
'''
    4.3添加
    生成ppot计算后的500组winp
    '''


def getdata(times):
    winrate = [0]*10 #30%~70%阶梯分布
    filename = '../data_dealing/500data/testdata_ppot0409.txt'  # 建立测试文本文档
    with open(filename, 'w') as f:
        for _ in range(times) :
            print("啦",end="")
            cards = [_ for _ in range(52)]
            random.shuffle(cards)
            our_cards = cards[0:2]
            board_cards = cards[2:5]
            del cards[0:5]
            rate = HS.get_winp(our_cards,board_cards)
            f.write(str(our_cards)+'\t')
            f.write(str(board_cards)+'\t')
            f.write(str(rate)+'\n')
    print("嘿！")

def get_p(our_cards,board_cards):
    cards = [_ for _ in range(52)]
    for a in our_cards:
        cards.remove(a)
    for b in board_cards:
        cards.remove(b)
    rate = HS.get_winp(our_cards, board_cards)
    print(rate)


if __name__ == "__main__":
    getdata(500)