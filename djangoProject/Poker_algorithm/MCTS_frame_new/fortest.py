import random
import Poker_algorithm.MCTS_frame_new.MCTS as MCT
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
    # 同样的，创建一个行为加权列表
    opp_action = opp_model.action_set[-1]
    our_strength = preflop_table[x][y]
    #print("actual_Post_strength: "+str(our_strength))
    # 聪明的人机不会放弃大盲注，所以对手跟到底池AI必然至少会跟注，即action_set≡0
    if opp_action == 2:
        for i in range(test_times):
            prediction = preflop_predict_post(opp_model)
            #print(prediction)
            if our_strength >= prediction+40:
                x = random.randint(1,10)
                if x > 2:
                    action_set[2]+=1
                continue
            if our_strength >= prediction-50:
                x = random.randint(1,10)
                if x > 3:
                    action_set[1]+=1
                continue
            x = random.randint(1,5)
            if x > 2:
                action_set[0]+=1
            else:
                action_set[1]+=1
        #print("action_set: "+str(action_set))
        our_action = 0
        testnum = random.randint(1,sum(action_set))
        for act in action_set:
            if testnum > act:
                our_action += 1
                testnum -= act
            else: break
    if opp_action == 1:
        for i in range(test_times):
            prediction = preflop_predict_post(opp_model)
            if our_strength >= prediction+30:
                action_set[2]+=1
                continue
            action_set[1]+=1
        #print(action_set)
        our_action = 0
        testnum = random.randint(1, test_times)
        for act in action_set:
            if testnum > act:
                our_action += 1
                testnum -= act
            else: break
    if our_action == 2:
        amount = MCT.calculate_raise_amount(action_set)
    return our_action, amount