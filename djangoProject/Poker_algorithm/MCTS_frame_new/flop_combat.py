import Poker_algorithm.MCTS_frame_new.preflop_combat as pref_cbt
import Poker_algorithm.MCTS_frame_new.MCTS as MCTS
import random
import Poker_algorithm.MCTS_frame_new.preflop_data as preflop_data
import Poker_algorithm.EHS_compare.compare_func as cmp
import Poker_algorithm.MCTS_frame_new.table_after_flop as taf
'''
Bug report in 7.29
1. 极少数情况出现的无限循环情况，在flop_pre操作出现
2. flop_post牌力分布恰好反了过来...传参可能有问题（已修复
'''
def refresh_preflop_for_pre(opp_model, our_model, our_deck, preflop_table):
    '''
    :param opp_model: 对手模型
    :param our_model: 自己的模型
    :param our_deck: 己方视角内的牌库
    :return: 刷新对手(对于先手方)可能牌型，该算法循环十次统计牌型满足次数来赋权重
    '''
    basecounter = len(opp_model.bet_amount)
    # 加注n次，总共经历n+1个回合
    if len(opp_model.bet_amount) > 1:
        # 持续加注和不存在持续加注是两种情况分别讨论
        # temp_model = our_model
        temp_model = MCTS.Opponent_Model()
        temp_model.action_set = opp_model.action_set  # 9.5加
        # 临时模型的创建，在后手决策内会排除重叠部分，这样复杂度更低
        deck = [i for i in range(52)]
        pref_cbt.refresh_preflop_for_post(temp_model, deck, preflop_table)
        for m in range(10):
            for i in our_deck:
                for j in our_deck:
                    if i == j :
                        continue
                    counter = basecounter
                    if pref_cbt.preflop_post([i, j], preflop_table, temp_model, 1)[0] <= 1:
                        continue
                    elif pref_cbt.preflop_post([i, j], preflop_table, temp_model, 1)[0] == 2:
                        satisfied = 1  # 判断该次抽样对应决策结果是否与对手行为相符
                        for m in range(counter):
                            if pref_cbt.preflop_afterward([i,j], preflop_table, temp_model, 1)[0] != 2:
                                satisfied = 0
                                break
                        if satisfied:
                            opp_model.possible_set.append([i,j])
    else:
        # temp_model = our_model  # (9.5f)修改为opp_model
        temp_model = MCTS.Opponent_Model()  # 9.5临时修改
        temp_model.action_set = opp_model.action_set  #9.5加
        deck = [i for i in range(52)]
        pref_cbt.refresh_preflop_for_post(temp_model, deck, preflop_table)
        for m in range(8):
            for i in our_deck:
                for j in our_deck:
                    if i == j:
                        continue
                    opp_deck = list(our_deck)
                    opp_deck.remove(i)
                    opp_deck.remove(j)
                    if pref_cbt.preflop_post([i, j], preflop_table, temp_model, 1)[0] == 1:
                        # our_model改成opp_model(9.4f)，9，5又改成temp
                        opp_model.possible_set.append([i,j])


'''
上两个函数为flop阶段的对手模型建立
'''
def flop_pre(opp_model, our_deck, our_cards, board_cards ,test_times):
    """
    flop 先手决策函数
    :param opp_model:
    :param our_deck:
    :param our_cards:
    :param board_cards:
    :param test_times:
    :return:
    """
    strength_set = [0,0,0]
    for i in range(test_times):
        opp_cards = random.choice(opp_model.possible_set)
        test_deck = list(our_deck)
        try:
            for card1 in opp_cards:
                test_deck.remove(card1)
            two_cards = random.sample(test_deck, 2)
        except BaseException:
            continue
        print("our:"+str(our_cards))
        print("opp:"+str(opp_cards))
        print("bc"+str(board_cards+two_cards))
        judge = cmp.Judgement(our_cards, opp_cards, board_cards+two_cards)
        strength_set[2-judge.status]+=1
    #print(strength_set) # for test
    action_set = [int(0.6 * strength_set[0]),
                  int(0.4 * (strength_set[0]) + 0.4 * (strength_set[2])) + strength_set[1],
                  int(0.6 * strength_set[2])]
    #print(action_set) # for test
    m = random.randint(1, sum(action_set))
    action = 0
    for act in action_set:
        m -= act
        if m < 0:
            break
        action += 1
    amount = 0
    if action == 2:
        amount = MCTS.calculate_raise_amount(strength_set)
    if action == 0:
        action = 1 # flop_pre不跟白不跟，AI不会犯傻！
    return action,amount



def refresh_flop_for_post(opp_model, board_cards, preflop_table):
    """
    此方法为preflop阶段后
    :param opp_model: 对手模型，要用到对手的第一步和第二步操作
    :param board_cards: 场上的公共牌
    :param preflop_table: 表格不赘述
    :return: 刷新对手模型的possible_set
    第二次刷新建立在第一次的权值基础上（已经有四万多组了
    可能会牺牲一定精度（但好像也不会
    """
    #print(len(opp_model.possible_set))
    '''现在按照zmx的思路，将牌型整体分为四种情况
    case1: 平稳-->平稳（筛选后选择较激进打法）
    case2: 平稳-->强势（筛选后选择较保守打法）
    case3: 强势-->强势（筛选后选择较保守打法）
    case4: 强势-->平稳（筛选后选择较激进打法）
    ps分布情况
    [21, 42, 127, 255, 361, 489, 638, 851, 957, 1085, 1241, 1319, 
    1411, 1603, 1752, 1844, 1936, 1993, 2022, 2078, 2107, 2114, 
    2178, 2185, 2206, 2206, 2224, 2224, 2224, 2234, 2234, 2245, 
    2245, 2245, 2256, 2256, 2266, 2266, 2266, 2277, 2277, 2288, 
    2288, 2288, 2298, 2298, 2309, 2320, 2320, 2320, 2320, 2330, 
    2330, 2330, 2341, 2341, 2351]
    '''
    new_set = []
    flop_table = taf.new_table(board_cards, 40)
    if opp_model.action_set[0] == 1:
        #print("111111111111")
        if opp_model.action_status == 1:
            # case1：
            for cards in opp_model.possible_set:
                card1 = cards[0]
                card2 = cards[1]
                if card1 in board_cards or card2 in board_cards:
                    continue
                if flop_table[card1][card2] > preflop_table[card1][card2] + 70:
                    i = random.randint(1,3)
                    if i>2:
                        new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2] + 50:
                    i = random.randint(1,5)
                    if i > 2:
                        new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2] + 30:
                    i = random.randint(1, 5)
                    if i > 1:
                        new_set.append(cards)
                else: new_set.append(cards)
            #print(len(opp_model.possible_set))  #for test
            opp_model.possible_set = new_set
            #print(len(opp_model.possible_set))  # for test
        # case2/3/4 仅进行参数调整
        if opp_model.action_status == 2:
            # case1：
            for cards in opp_model.possible_set:
                card1 = cards[0]
                card2 = cards[1]
                if flop_table[card1][card2] > preflop_table[card1][card2] + 100:
                    i = random.randint(1,7)
                    if i > 2:
                        new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2] + 70:
                    i = random.randint(1,7)
                    if i > 3:
                        new_set.append(cards)
                elif flop_table[card1][card2] > 750:
                    i = random.randint(1, 7)
                    if i > 2:
                        new_set.append(cards)
                elif flop_table[card1][card2] > 720:
                    i = random.randint(1, 3)
                    if i > 1:
                        new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2] + 20:
                    i = random.randint(1, 5)
                    if i > 2:
                        new_set.append(cards)
                else:
                    i = random.randint(1,3)
                    if i > 2:
                        new_set.append(cards)
            #print(len(opp_model.possible_set))  # for test
            opp_model.possible_set = new_set
            #print(len(opp_model.possible_set))  # for test



    if opp_model.action_set[0] == 2:
        if opp_model.action_status == 1:
            # case1：
            for cards in opp_model.possible_set:
                card1 = cards[0]
                card2 = cards[1]
                if flop_table[card1][card2] > preflop_table[card1][card2] + 100:
                    i = random.randint(1,3)
                    if i > 2:
                        new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2] + 50:
                    i = random.randint(1,5)
                    if i > 2:
                        new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2]:
                    i = random.randint(1, 5)
                    if i > 1:
                        new_set.append(cards)
                elif flop_table[card1][card2] > 740:
                    i = random.randint(1, 5)
                    if i > 2:
                        new_set.append(cards)
                else:
                    new_set.append(cards)
            #print(len(opp_model.possible_set))  #for test
            opp_model.possible_set = new_set
            #print(len(opp_model.possible_set))  # for test
        # case4
        if opp_model.action_status == 2:
            for cards in opp_model.possible_set:
                card1 = cards[0]
                card2 = cards[1]
                if flop_table[card1][card2] > preflop_table[card1][card2] + 100:
                    new_set.append(cards)
                elif flop_table[card1][card2] > 770:
                    new_set.append(cards)
                elif flop_table[card1][card2] > preflop_table[card1][card2] + 30:
                    i = random.randint(1, 4)
                    if i > 1:
                        new_set.append(cards)
                elif flop_table[card1][card2] < 700:
                    i = random.randint(1, 7)
                    if i > 5:
                        new_set.append(cards)
                else:
                    i = random.randint(1,3)
                    if i > 2:
                        new_set.append(cards)
            #print(len(opp_model.possible_set))  # for test
            opp_model.possible_set = new_set
            #print(len(opp_model.possible_set))  # for test




def flop_post(opp_model, our_cards, our_deck, board_cards ,preflop_table, test_times):

    refresh_flop_for_post(opp_model, board_cards, preflop_table)
    # 7.10 日版本更改注释，因为flop后手的函数需要两次更新对手模型，
    # preflop阶段的模型更新选择的action变为actionset的第一位
    # 7.12 日，对手模型的刷新实现，接下来按照模型进行内部随机抽样，同flop_pre的操作
    strength_set = [0, 0, 0]
    for i in range(test_times):
        opp_cards = random.choice(opp_model.possible_set)
        test_deck = list(our_deck)
        try:
            for card1 in opp_cards:
                test_deck.remove(card1)
        except BaseException:
            continue
        # 有个bug，但我强行跳过了
        two_cards = random.sample(test_deck, 2)
        judge = cmp.Judgement(our_cards, opp_cards, board_cards + two_cards)
        strength_set[2 - judge.status] += 1
    #print(strength_set)
    opp_model.distribution = strength_set
    action_set = []
    if opp_model.action_status == 2:
        action_set = [int(0.7 * strength_set[0]),
                      int(0.3 * (strength_set[0]) + 0.7 * (strength_set[2])) + strength_set[1],
                      int(0.3 * strength_set[2])]
    if opp_model.action_status == 1:
        action_set = [int(0.7 * strength_set[0]),
                      int(0.3 * (strength_set[0]) + 0.3 * (strength_set[2])) + strength_set[1],
                      int(0.7 * strength_set[2])]
    # 7.12 调整方式初步思考，根据对手上轮加注数量而进行改动，但加注数目暂时未引入
    #print(action_set)
    amount = 0
    m = random.randint(1, sum(action_set))
    action = 0
    for act in action_set:
        m -= act
        if m < 0:
            break
        action += 1
    if opp_model.action_set[-1] == 1 and action == 0:
        action = 1 # 和上面同理
    if action == 2:
        amount = MCTS.calculate_raise_amount(action_set)
    return action, amount



def flop_afterward():
    pass



if __name__ == "__main__":
    preflop_table = preflop_data.get_table()
    pre_player = MCTS.Opponent_Model()
    post_player = MCTS.Opponent_Model()
    post_player.action_set = [1]
    pre_player.action_set = [2]
    deck_cards = [i for i in range(52)]
    deck = list(deck_cards)
    actual_deck = list(deck)
    pre_cards = random.sample(deck_cards, 2)
    post_cards = random.sample(deck, 2)
    print("pre_cards:  " + str(pre_cards))
    print("post_cards:  " + str(post_cards))
    for x in pre_cards:
        deck_cards.remove(x)
        actual_deck.remove(x)
    for x in post_cards:
        deck.remove(x)
        actual_deck.remove(x)
    pre_deck = list(deck_cards)
    post_deck = list(deck)
    board_cards = random.sample(actual_deck, 3)
    for card in board_cards:
        actual_deck.remove(card)
    flop_pre(post_player, pre_deck, pre_cards, board_cards ,5000)
    flop_post(pre_player, post_cards, post_deck, board_cards, preflop_table, 5000)