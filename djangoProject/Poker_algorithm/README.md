# Poker-algorithm
## from FuncToUse import FuncInstruction as F
FuncInstruction是可以直接调用的方法汇总文件，包括：
1. get_MTC_EHS_and_types(my_cards, pub_cards)
    返回由蒙特卡洛抽样得到的胜率以及各牌型预测概率。已与枚举得到的正确结果对比，误差范围在10^-3,运行时间约5s
2. get_type(cards)
    5~7张牌均可，为固定牌型分析。返回值对应：0-皇家同花顺；1-同花顺；2-四条；3-葫芦；4-同花；5-顺子；6-三条；7-两对；8-一对；9-高牌
3. get_acEHS(my_cards, pub_cards)
    得到完全枚举出的准确胜率
4. get_n_acEHS(my_cards, pub_cards, n)
    得到有n个对手（但默认对手行动呆板完全随机）的胜率
5. get_acHP(my_cards, pub_cards)
    得到完全枚举出的P_Pot，N_Pot，HS。用于计算EHS，一般不会用到。
6. get_cards_score(my_cards,pub_cards)
	得到牌力值