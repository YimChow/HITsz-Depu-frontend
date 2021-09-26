import Poker_algorithm.MCTS_frame_new.table_after_flop as taf
import Poker_algorithm.MCTS_frame_new.MCTS as MCTS
import Poker_algorithm.MCTS_frame_new.preflop_data as preflop_data
import random
import Poker_algorithm.MCTS_frame_new.flop_combat as fc
import Poker_algorithm.EHS_compare.compare_func as cmp

def refresh_flop_for_pre(opp_model, board_3_cards, turn_card, preflop_table):
    '''
    刷新对手经过两轮操作后的对手模型
    :param board_3_cards: 三张牌
    :return: 刷新后的对手模型
    其实和前面的refresh_flop_for_post有些
    '''
    fc.refresh_flop_for_post(opp_model, board_3_cards, preflop_table)
    #print("before refresh model_length: "+ str(len(opp_model.possible_set)))
    if len(opp_model.possible_set) > 10000:
        new_set = random.sample(opp_model.possible_set, 10000)
        opp_model.possible_set = new_set
        # 避免加注后复杂度爆炸

    temp_set = list(opp_model.possible_set)
    for cards in opp_model.possible_set:
        if cards[0] == turn_card[0] or cards[1] == turn_card[0]:
            #print("remove: "+str(cards))
            temp_set.remove(cards)
    opp_model.possible_set = temp_set
    #print("after refresh model_length: "+ str(len(opp_model.possible_set)))


def turn_pre(opp_model, our_cards, board_4_cards, our_deck):
    #refresh_flop_for_pre(opp_model, board_3_cards, preflop_table)
    strength_set = [0,0,0]
    for opp_cards in opp_model.possible_set:
        temp_deck = list(our_deck)
        for card in opp_cards:
            temp_deck.remove(card)
            # 出现bug： x not in list
            # 修复：原因是turn牌可能是set中的牌
        for i in temp_deck:
            river_card = [i]
            judge = cmp.Judgement(our_cards, opp_cards, board_4_cards+river_card)
            strength_set[2-judge.status] += 1
    #print(strength_set)

    opp_model.distribution = strength_set
    # 7.19瓶颈问题：
    # 决策函数的actionset将会由status来替代，而划分的系数将不再是一个常数，而是用一个含加注数目的参数
    action_set = [int(0.6 * strength_set[0]),
                  int(0.4 * (strength_set[0]) + 0.4 * (strength_set[2])) + strength_set[1],
                  int(0.6 * strength_set[2])]
    #print(action_set)
    m = random.randint(1, sum(action_set))
    action = 0
    amount = 0
    for act in action_set:
        m -= act
        if m < 0:
            break
        action += 1
    if action == 0:
        action = 1
    if action == 2:
         amount = MCTS.calculate_raise_amount(action_set)
    return action, amount



def refresh_rest(opp_model, board_before, added_card):
    board_after = board_before + added_card
    table_before_turn = taf.new_table(board_before, 1)
    #当有四张牌的时候，后面的参数是没必要添加的，会自动遍历所有
    #从这个决策阶段开始，计算出来的将都是精确值，而且不需要prefloptable了
    table_after_turn = taf.new_table(board_after, 1)
    #前后的两个表中对应的位置的值影响决策的方式
    new_set = []
    #print(len(opp_model.possible_set))
    if opp_model.action_status == 1:
        for cards in opp_model.possible_set:
            x = cards[0]
            y = cards[1]
            if table_after_turn[x][y] >= 770 and table_after_turn[x][y] <= table_before_turn[x][y] + 20:
                i = random.randint(1,5)
                if i > 1:
                    new_set.append(cards)
            elif table_after_turn[x][y] <= table_before_turn[x][y]:
                i = random.randint(1,3)
                if i > 1 :
                    new_set.append(cards)
            elif table_after_turn[x][y] >= table_before_turn[x][y] + 20:
                i = random.randint(1,5)
                if i > 2:
                    new_set.append(cards)
            else:
                i = random.randint(1,7)
                if i > 3:
                    new_set.append(cards)

    if opp_model.action_status == 2:
        new_set = []

        for cards in opp_model.possible_set:
            x = cards[0]
            y = cards[1]
            if table_after_turn[x][y] >= 770:
                new_set.append(cards)
            elif table_after_turn[x][y] >= table_before_turn[x][y] and table_after_turn[x][y] >= 750:
                new_set.append(cards)
            elif table_after_turn[x][y] >= 750:
                i = random.randint(1,5)
                if i>1:
                    new_set.append(cards)
            elif table_after_turn[x][y] >= 730:
                i = random.randint(1,5)
                if i > 2:
                    new_set.append(cards)
            elif table_after_turn[x][y] < 700:
                i = random.randint(1,5)
                if i > 4:
                    new_set.append(cards)
            else:
                i = random.randint(1,5)
                if i > 3:
                    new_set.append(cards)
    opp_model.possible_set = new_set
    temp_set = list(opp_model.possible_set)
    for cards in opp_model.possible_set:
        if cards[0] == added_card or cards[1] == added_card:
            # print("remove: "+str(cards))
            temp_set.remove(cards)
    opp_model.possible_set = temp_set
    if len(opp_model.possible_set) > 10000:
        temp_set = random.sample(opp_model.possible_set, 10000)
        opp_model.possible_set = temp_set



def turn_post(our_cards, our_deck, board_4_cards, opp_model):
    strength_set = [0, 0, 0]
    for opp_cards in opp_model.possible_set:
        temp_deck = list(our_deck)
        for i in temp_deck:
            river_card = [i]
            judge = cmp.Judgement(our_cards, opp_cards, board_4_cards + river_card)
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
    #print(action_set)
    m = random.randint(1, sum(action_set))
    action = 0
    amount = 0
    for act in action_set:
        m -= act
        if m < 0:
            break
        action += 1
    if action == 0 and opp_model.action_set[-1] == 1:
        action = 1
    if action == 2:
        amount = MCTS.calculate_raise_amount(action_set)
    return action, amount

# mark


def river_pre(our_cards, board_5_cards, opp_model):
    # 不再需要己方视角的牌库，因为数据已经完全已知
    strength_set = [0,0,0]
    for opp_cards in opp_model.possible_set:
        judge = cmp.Judgement(our_cards, opp_cards, board_5_cards)
        strength_set[2 - judge.status] += 1
    #print(strength_set)
    action_set = [int(0.6 * strength_set[0]),
                  int(0.4 * (strength_set[0]) + 0.4 * (strength_set[2])) + strength_set[1],
                  int(0.6 * strength_set[2])]
    #print(action_set)
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
        action = 1
    return action, amount

def river_post(our_cards, board_5_cards, opp_model):
    strength_set = [0,0,0]
    for opp_cards in opp_model.possible_set:
        judge = cmp.Judgement(our_cards, opp_cards, board_5_cards)
        strength_set[2 - judge.status] += 1
    #print(strength_set)
    action_set = []
    if opp_model.action_status == 2:
        action_set = [int(0.7 * strength_set[0]),
                      int(0.3 * (strength_set[0]) + 0.7 * (strength_set[2])) + strength_set[1],
                      int(0.3 * strength_set[2])]
    if opp_model.action_status == 1:
        action_set = [int(0.7 * strength_set[0]),
                      int(0.3 * (strength_set[0]) + 0.3 * (strength_set[2])) + strength_set[1],
                      int(0.7 * strength_set[2])]
    #print(action_set)
    m = random.randint(1, sum(action_set))
    action = 0
    amount = 0
    for act in action_set:
        m -= act
        if m < 0:
            break
        action += 1
    if action == 0 and opp_model.action_set[-1] == 1:
        action = 1
    if action == 2:
        amount = MCTS.calculate_raise_amount(action_set)
    return action, amount








if __name__ == "__main__":
    opp_model = MCTS.Opponent_Model()
    our_cards = [5,10]
    board_3_cards = [1,2,3]
    board_4_cards = [1,2,3,4]
    our_deck = [13]
    preflop_table = preflop_data.get_table()
