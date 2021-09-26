import random
import Poker_algorithm.MCTS_frame_new.MCTS as MCT
import Poker_algorithm.MCTS_frame_new.preflop_data as preflopdata

'''
7.7日实现：
重构后的preflop操作（复杂了很多
实现了概率性决策以及加权的概率性分析

'''

def uncertain_pre_preflop(cards, preflop_table):
    """
    :param cards:
    :return: action_possible_set: [x,y,z]
    对应 弃牌，跟注，加注, x+y+z=100,用随机数抽取进行决策
    [xxx...xxxx[yyyyy....yyyy]zzzz...zzz],看落入的区间
    待提升的: 加入筹码的维度（暂时还未实现）
    """
    x = cards[0]
    y = cards[1]
    strength = preflop_table[x][y]
    #print("actual_Pre_strength: "+str(strength))
    # 阈值：675 705 725 735 755 775 800
    if strength>800:
        return [0,25,100]
    if strength>775:
        return [0,30,100]
    if strength>755:
        return [0,50,100]
    if strength>735:
        return [0,60,100]
    if strength>725:
        return [0,80,100]
    if strength>705:
        return [5,90,100]
    if strength>675:
        return [15,100,100]
    return [40,100,100]

def preflop_pre(cards, preflop_table):
    m = random.randint(1,100)
    amount = 0
    uct_set = uncertain_pre_preflop(cards, preflop_table)
    action = 0
    for act in uct_set:
        if m>act:
            action += 1
    if action == 2:
        distribution = [uct_set[0],uct_set[1]-uct_set[0],uct_set[2]-uct_set[1]]
        amount = MCT.calculate_raise_amount(distribution)
    return action, amount


def refresh_preflop_for_post(opp_model, our_deck, preflop_table):
    '''
    :param opp_model: 对手模型
    :param preflop_table:
    :param our_deck: 己方视角的牌库
    :return: 刷新对手(对于后手方)可能牌型，注意对手所有牌型的可能性均考虑，这里选择降低权重处理
    '''
    # 8.10 修复了个离谱的bug
    opp_model.possible_set = []
    if opp_model.action_status == 1:
        for i in our_deck:
            for j in our_deck:
                if preflop_table[i][j] >= 775:
                    for m in range(3): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 755:
                    for m in range(5): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 735:
                    for m in range(6): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 725:
                    for m in range(8): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 705:
                    for m in range(8): opp_model.possible_set.append([i, j])
                elif preflop_table[i][j] >= 675:
                    for m in range(7): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 650:
                    for m in range(6): opp_model.possible_set.append([i,j])







    if opp_model.action_status == 2:
        for i in range(52):
            for j in range(52):
                if preflop_table[i][j] >= 800:
                    for m in range(15): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 775:
                    for m in range(14): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 755:
                    for m in range(10): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 735:
                    for m in range(8): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 725:
                    for m in range(4): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 705:
                    for m in range(2): opp_model.possible_set.append([i,j])
                elif preflop_table[i][j] >= 650:
                    for m in range(1): opp_model.possible_set.append([i,j])







'''
# 此决策模式已经放弃使用 --7.29
def preflop_predict_post(opp_model):
    """
    :param opp_model: 对手模型：主要调用对手的行为
    :return: 此次估计的对手牌力（区间取下界
    """
    action = opp_model.action_set[-1]

    if action == 1:
        # 加权抽样思路同上
        uct_set = [60, 145, 230, 310, 370, 420, 450, 475]
        uct_dic = [650, 675, 705, 725, 735, 755, 775, 800]
        # 分别为权值分布列表和对应牌力列表（均为左边界，保持较悲观估计，取较左的为参考值
        m = random.randint(0, 475)
        estimate = 0
        for n in uct_set:
            if m > n: estimate += 1
        #print("predict_strength: " + str(uct_dic[estimate]))
        return uct_dic[estimate]
    if action == 2:
        uct_set = [10, 30, 70, 120, 190, 265]
        uct_dic = [705, 725, 735, 755, 775, 800]
        # 分别为权值分布列表和对应牌力列表（均为左边界，保持较悲观估计，取较左的为参考值
        m = random.randint(0, 265)
        estimate = 0
        for n in uct_set:
            if m > n: estimate += 1
        #print("predict_strength: " + str(uct_dic[estimate]))
        return uct_dic[estimate]
'''

def preflop_post(our_cards, preflop_table, opp_model, test_times):
    """
    :param our_cards: 手牌会被多次调用
    :param preflop_table: 对照牌力表
    :param opp_model: 对手模型
    :param test_times: 抽样次数，与精度有关，可以任意设置
    :return: our_action本轮行动
    该函数在后续还要添加对手模型筛选，初步构想是形成52*52存储0-9的数表示权重（形式待定
    """
    x = our_cards[0]
    y = our_cards[1]
    action_set = [0,0,0]
    amount = 0
    our_action = 0
    our_strength = preflop_table[x][y]
    #print(len(opp_model.possible_set))
    #refresh_preflop_for_post(opp_model, our_deck, preflop_table)
    # 7.26为了优化代码结构，refresh可能将不再写入函数内
    for i in range(test_times):
        # bug report: 后手加注bug：对手建模为空
        opp_cards = random.choice(opp_model.possible_set)
        while opp_cards[0] == x or opp_cards[1] == x\
                or opp_cards[1] == y or opp_cards[1] == y:
            opp_cards = random.choice(opp_model.possible_set)
            # 消除重复卡带来的bug，这一个步骤主要是在重构flop pre的时候降低时间复杂度
        if preflop_table[opp_cards[0]][opp_cards[1]] >= our_strength + 40:
            action_set[0] += 2
            action_set[1] += 1
        elif our_strength >= preflop_table[opp_cards[0]][opp_cards[1]] + 40:
            action_set[2] += 2
            action_set[1] += 1
        else:
            action_set[1] += 3
    #print(action_set)
    i = random.randint(1,sum(action_set))
    for x in range(3):
        if action_set[x] > i:
            break
        i -= action_set[x]
        our_action += 1
    # 下面这个判断仅限二人对战，多人对战要引入玩家编号的属性，判断要附加条件
    if our_action == 0 and opp_model.action_set[-1] == 1:
        our_action = 1  # 小盲注下注，大盲注没有不跟注的理由
    # end
    if our_action == 2:
        amount = MCT.calculate_raise_amount(action_set)
    return our_action, amount


def preflop_afterward(our_cards, preflop_table, opp_model, test_times):
    """
        :param our_cards: 手牌会被多次调用
        :param preflop_table: 对照牌力表
        :param opp_model: 对手模型
        :param test_times: 抽样次数，与精度有关，可以任意设置
        :return: our_action本轮行动
        该函数在后续还要添加对手模型筛选，初步构想是形成52*52存储0-9的数表示权重（形式待定
        """
    x = our_cards[0]
    y = our_cards[1]
    action_set = [0, 0, 0]
    amount = 0
    our_action = 0
    our_strength = preflop_table[x][y]
    for i in range(test_times):
        opp_cards = random.choice(opp_model.possible_set)
        if preflop_table[opp_cards[0]][opp_cards[1]] >= our_strength + 40:
            action_set[0] += 2
            action_set[1] += 1
        elif our_strength >= preflop_table[opp_cards[0]][opp_cards[1]] + 40:
            action_set[2] += 2
            action_set[1] += 1
        else:
            action_set[1] += 3
    # print(action_set)
    i = random.randint(1, sum(action_set))
    for x in range(3):
        if action_set[x] > i:
            break
        i -= action_set[x]
        our_action += 1

    if our_action == 2:
        amount = MCT.calculate_raise_amount(action_set)
    return our_action, amount


    
    



if __name__ == "__main__":
    preflop_table = preflopdata.get_table()
    x_model = MCT.Opponent_Model()
    y_model = MCT.Opponent_Model()
    # x_model: player1 模型；  y_model: player2 模型
    deck_cards = [i for i in range(52)]
    deck = list(deck_cards)
    for i in range(10):
        x_cards = random.sample(deck_cards,2)
        y_cards = random.sample(deck,2)
        print("x_cards:  "+str(x_cards))
        print("y_cards:  "+str(y_cards))
        for x in x_cards:
            deck_cards.remove(x)
        for x in y_cards:
            deck.remove(x)
        x_deck = list(deck_cards)
        y_deck = list(deck)
        # 测试起牌准备工作
        action = preflop_pre(x_cards,preflop_table)
        print("preflop_pre_action:" + str(action))
        if action == 0:
            print(" ")
            continue
        x_model.action_set.append(action)
        our_action = preflop_post(y_cards ,preflop_table,x_model,200)
        print("preflop_post_action: " + str(our_action))
        print(" ")

