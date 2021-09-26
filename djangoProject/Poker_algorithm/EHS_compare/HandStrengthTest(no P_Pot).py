
from EHS_compare import compare_func as com
import random
'''
    4.3添加
    生成概率均匀分布的测试数据
    '''
#def mtkl_test(time2,our_card,board_card,card):
'''
    半成品无视就好
    :param time2:抽样次数
    :param our_card:我们的牌
    :param board_card:公共牌
    :param card:牌池
    :return:蒙特卡洛抽样胜率
    '''
'''   win_rp = 0                          # win rp计算(抽样胜率)
    for j in range(time2):
        other_cards = random.sample(cards2, 4)
        two_pub_cards = other_cards[0:2]
        opp_cards = other_cards[2:4]
        judge = com.Judgement(our_cards,opp_cards,public_cards+two_pub_cards)
        if judge.status == 0:
            win_rp += 1
        elif judge.status == 1:
            win_rp += 0.5

#f.write(str(our_cards)+'\t')
#f.write(str(public_cards)+'\t')
#f.write(str(win_rp/time2)+'\t')
#f.write(str(win_p)+'\n')
'''





def getdata():
    winrate = [0]*10 #30%~70%阶梯分布
    filename = 'testdata.txt'   # 建立测试文本文档
    with open(filename, 'w') as f:
        for _ in range(10) :
            cards = [_ for _ in range(52)]
            random.shuffle(cards)
            our_cards = cards[0:2]
            board_cards = cards[2:5]
            del cards[0:5]
            win1 = 0
            for i in range (47):
                for j in range (i+1, 47):
                    opp_cards = [cards[i], cards[j]]
                    for k in range(47):
                        if k != i and k != j:
                            for _q in range(k + 1, 47):
                                if _q != j and _q != i:
                                    board_cards2 = board_cards + [cards[k], cards[_q]]
                                    win1 += 0.5*com.Judgement(our_cards,opp_cards,board_cards2).status
            rate = 1-win1/(23*47*45*22)
            f.write(str(our_cards)+'\t')
            f.write(str(board_cards)+'\t')
            f.write(str(rate)+'\n')


def testdata(our_cards,board_cards,cards):
    win1 = 0
    for i in range(47):
        for j in range(i + 1, 47):
            opp_cards = [cards[i], cards[j]]
            for k in range(47):
                if k != i and k != j:
                    for _q in range(k + 1, 47):
                        if _q != j and _q != i:
                            board_cards2 = board_cards + [cards[k], cards[_q]]
                            win1 += 0.5 * com.Judgement(our_cards, opp_cards, board_cards2).status
    rate = 1-(win1 / (23 * 47 * 45 * 22))
    print(rate)

def testcards(cardsa, cardsb, cards):
    cards = [_ for _ in range(52)]
    for i in cardsa:
        cards.remove(i)
    for j in cardsb:
        cards.remove(j)
    testdata(cardsa, cardsb, cards)


if __name__ == "__main__":
    #getdata()
    cards= [_ for _ in range(52)]
    testcards([17, 28], [20, 40, 21], cards)
    testcards([18, 35], [21, 48, 20], cards)
    testcards([28, 20], [9, 24, 5], cards)
    testcards([20, 0], [7, 8, 31], cards)
    testcards([22, 20], [47, 45, 35], cards)
    testcards([32, 40], [51, 44, 33], cards)
    testcards([24, 47], [11, 15, 31], cards)
    testcards([8, 48], [41, 25, 26], cards)
    testcards([9, 43], [47, 12, 21], cards)