"""
第二层封装
"""
from Poker_algorithm.EHS_compare import compare_func as com
import random


def get_winp(my_cards,public_cards):       # 初值条件为2+3的获得3*3模型的winning_percentage 函数
    Package = HP(my_cards,public_cards)    # 将手牌和公共牌初步计算出两轮Hand Potential
    P_Pop,N_Pop,HS = Package               # Positve/Negative && handstrength
    win_p = HS*(1-N_Pop) + (1-HS)*P_Pop    # 根据公式计算winning_percentage
    return win_p

def random_sample(time1,time2):
    '''
    3.29添加
    :param time1: 起牌次数
    :param time2: 测试次数（对于每次起牌而言）
    :return:输出至time2_static.txt
    '''
    cards = [_ for _ in range(52)]


    filename = str(time2) + 'static.txt'   # 建立测试文本文档
    with open(filename, 'w') as f:
        for i in range(time1):
            known_cards = random.sample(cards, 5)
            cards2 = [_ for _ in range(52) ]
            for x in known_cards:
                cards2.remove(x)

            our_cards = known_cards[0:2]
            public_cards = known_cards[2:5]     # 模拟发牌并且计算出胜率winp
            win_p = get_winp(our_cards, public_cards)
            win_rp = 0                          # win rp计算(抽样胜率)
            for j in range(time2):
                other_cards = random.sample(cards2, 4)
                two_pub_cards = other_cards[0:2]
                opp_cards = other_cards[2:4]
                judge = com.Judgement(our_cards,opp_cards,public_cards+two_pub_cards)
                if judge.status == 0:
                    win_rp += 1
                elif judge.status == 1:
                    win_rp += 0.5
                print(i, j / time2)            # 计数算得抽样胜率

            f.write(str(our_cards)+'\t')
            f.write(str(public_cards)+'\t')
            f.write(str(win_rp/time2)+'\t')
            f.write(str(win_p)+'\n')





def HS(our_cards, board_cards):
    cards = [_ for _ in range(52)]
    known_cards = our_cards + board_cards
    for _ in known_cards:
        cards.remove(_)
    triple = [0]*3      # [ahead, tied, behind]
    opp_types = [0]*10

    # enumerate all of the opponent hands
    for i in range(47):
        for j in range(i+1, 47):
            opp_cards = [cards[i], cards[j]]
            judge = com.Judgement(our_cards, opp_cards, board_cards)
            triple[judge.status] += 1

    hand_strength = (triple[0]+triple[1]/2)/sum(triple)
    return hand_strength  # 后两个是测试用的


def HP(our_cards, board_cards):
    cards = [_ for _ in range(52)]
    known_cards = our_cards + board_cards
    for _ in known_cards:
        cards.remove(_)
    hp = [[0,0,0],[0,0,0],[0,0,0]] # [ahead, tied, behind]
    hp_total = [0]*3
    opp_types = [0] * 10
    my_types = [0]*10

    test = [0]*3

    # enumerate all of the opponent hands
    for i in range(47):
        for j in range(i + 1, 47):
            opp_cards = [cards[i], cards[j]]
            judge = com.Judgement(our_cards, opp_cards, board_cards)

            for k in range(47):
                if k != i and k != j:
                    for _q in range(k+1, 47):
                        if _q != j and _q != i:
                            board_cards2 = board_cards+[cards[k], cards[_q]]
                            judge_2 = com.Judgement(our_cards, opp_cards, board_cards2)
                            my_types[judge_2.type] += 1
                            o = judge.status
                            l = judge_2.status
                            hp[o][l] += 1
                            hp_total[judge.status] += 1
                            test[l] += 1


    divis1 = (hp_total[2] + hp_total[1]/2)
    divis2 = (hp_total[0]+hp_total[1]/2)
    if divis1 != 0:
        p_pot = (hp[2][0]+hp[2][1]/2+hp[1][0]/2)/divis1
    else:
        p_pot = 1
    if divis2 != 0:
        n_pot = (hp[0][2] + hp[1][2]/2+hp[0][1]/2)/divis2
    else:n_pot = 1
    hand_strength = (hp_total[0]+hp_total[1]/2)/sum(hp_total)
    return p_pot, n_pot ,hand_strength   # ,hp_total,hp,test,my_types,opp_types


if __name__ == "__main__":
    #p = HS([50,41],[39,9,7])
    #print(p)
    jug = com.Judgement([50,41],[13,31],[39,9,7,49,1])
    print(jug.status)
    print(jug.opp_type,jug.type)


    q = HP([50,41],[39,9,7])
    # q = HP([41,35],[15,7,2])
    print(q)




    """
    test = com.Judgement([51,50],[47,46],[43,42,41,11,10])
    print(test.status)
    print(test.type)
    print(test.opp_type)
    """
    """
    cards = [_ for _ in range(52)]
    filename = "test_static"
    with open(filename,'w') as f:
        for i in range(52):
            for j in range(i+1,52):
                for k in range(j+1,52):
                    for n in range(k+1,52):
                        for l in range(n+1,52):
                            m = [[cards[i],cards[j]], [cards[k], cards[n], cards[l]]]
                            a = HS([cards[i],cards[j]], [cards[k], cards[n], cards[l]])
                            f.write(str(m))
                            f.write('\t')
                            f.write(str(a))
                            f.write('\n')

"""


