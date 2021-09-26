from Poker_algorithm.EHS_compare import HandStrength as HanStr
from Poker_algorithm.EHS_compare.Analysis_class import Analysis
from Poker_algorithm.EHS_compare.compare_func import Judgement
from Poker_algorithm.MTC_BasedOn_EHS import Winning_p_forecast as W
import random


def get_acHP(my_cards, pub_cards):
    """
    得到PPot、NPot、HS.
    其中，PPot：翻牌前落后但是翻牌后后来居上的概率
         NPot:翻牌前领先反后落后的概率
         HS：HandStrenth，the probability that a given hand is better than that of an active opponent.
    :param my_cards:[a,b] 序列为手牌值
    :param pub_cards:[a,b,c] 为桌面的三张公共牌
    :return: P_Pot、N_Pot、HS  作为一个包。
    """
    return HanStr.HP(my_cards, pub_cards)


def get_acEHS(my_cards, pub_cards):
    """
    准确概率实现双人胜率计算
    :param my_cards:[a,b] 序列为手牌值
    :param pub_cards:[a,b,c] 为桌面的三张公共牌
    :return:最终的胜率EHS = HS+(1-HS)*PPot
    """
    Package = get_acHP(my_cards, pub_cards)
    P_Pot, N_Pot, HS = Package
    return HS+(1-HS)*P_Pot


def get_n_acEHS(my_cards, pub_cards, n):
    """
    准确概率，假设每一个对手都一样可以得出一个EHS，而对不同对手不同风格有不同的EHSi = EHSi = HSi+(1-HSi)*PPot
    :param my_cards: [a,b] 手牌
    :param pub_cards: [a,b,c] 公共牌
    :param n: 对手的人数
    :return: EHS： EHS=HS^n+(1+HS^n)*PPot
    """
    Package = get_acHP(my_cards, pub_cards)
    P_Pot, N_Pot, HS = Package
    return HS**n + (1-HS**n)*P_Pot


def get_type(cards):
    """
    固定牌型分析；
    :param cards: [a,b,c,d,e,(f),(g)] 可以是5-7张牌的序列。
    :return: 0-皇家同花顺；1-同花顺；2-四条；3-葫芦；4-同花；5-顺子；6-三条；7-两对；8-一对；9-高牌
    """
    analyst = Analysis(cards)
    dic={"0":"皇家同花顺","1":"同花顺","2":"四条","3":"满堂红","4":"同花","5":"顺子","6":"三条","7":"两对","8":"一对","9":"高牌"}
    return dic[str(analyst.type())]


def get_MTC_EHS_and_types(my_cards, pub_cards):
    """
    获得蒙特卡洛抽样得到的胜率以及牌型预测
    :param my_cards: [a,b] 手牌
    :param pub_cards: [a,b,c] 公共牌
    :return: EHS,types[10]为对应以下牌型的概率 index = 0-皇家同花顺；1-同花顺；2-四条；3-葫芦；4-同花；5-顺子；6-三条；7-两对；8-一对；9-高牌

    """
    simulate_times = 10000 # 抽样次数
    forecaster = W.Forecaster(my_cards,pub_cards,simulate_times)
    Package = forecaster.HP()
    P_Pot, N_Pot, HS, types = Package
    return HS+(1-HS)*P_Pot, types


def get_cards_score(my_cards,pub_cards):
    """
    在WT的时候用牌力值就好了不用再抽样计算胜率了！然后就是这个牌力值只是为了区分大小，没有严格意义上的按真实牌力分布，起大概估计的作用
    :param my_cards: [a,b]两张
    :param pub_cards: [a,b,c,[d],[e]]   公共牌，3-5张
    :return:
    """
    analyst = Analysis(my_cards+pub_cards)
    type = analyst.type()
    score = (10-type)*2200 + analyst.judge[type]  # 牌力值
    '''7.1日改动，牌型对牌力影响减小了'''
    return score

def type_forcaster(known_cards):
    """
    返回对两张手牌的牌型预测
    :param known_cards: [a,b],或[a,b,c,d,e]或[a,b,c,d,e,f]
    :return: [a,b,...]十个str+%的概率
    """
    cards = [i for i in range(52)]
    for i in range(len(known_cards)):
        cards.remove(known_cards[i])

    random_cards = 7 - len(known_cards)
    prob = [0 for i in range(10)]
    simu_times = 10000
    ans = {}

    for i in range(simu_times):
        new_cards = random.sample(cards, random_cards)
        analyst = Analysis(known_cards+new_cards)
        the_type = analyst.type()
        prob[the_type] += 1
    for i in range(10):
        prob[i] = 100*(prob[i]/simu_times)
        ans[str(i)] = str(round(prob[i], 2))+'%'
    return ans


def opp_type_forcaster(self_cards,pub_cards):
    cards = [_ for _ in range(52)]
    for _ in self_cards+pub_cards:
        cards.remove(_)
    sim_time = 10000
    new_pub_cards = 5-len(pub_cards)
    prob = [0 for i in range(10)]
    ans = {}
    for i in range(sim_time):
        sample_cards = random.sample(cards, 2+new_pub_cards)
        analyst  = Analysis(sample_cards+pub_cards)
        the_type = analyst.type()
        prob[the_type] += 1
    for i in range(10):
        prob[i] = 100*(prob[i]/sim_time)
        ans[str(i)] = str(round(prob[i], 2))+'%'
    return ans


def is_win(self_cards,opp_cards,pub_cards):
    """
    判断是否获胜
    :param self_cards: 自己的牌
    :param opp_cards: 对手的牌
    :param pub_cards: 公共牌
    :return: ”0“，获胜，”1“，平局，”2“失败
    """
    jugement = Judgement(self_cards,opp_cards,pub_cards)
    return str(jugement.status)


# print(get_nEHS([23, 12], [45, 3, 21], 5)) 测试
# print(get_type([23,41,24,3,5,43])) 测试
# print(MTC_typesp_and_winp([2,4],[23,51,19,46])) 测试