import Poker_algorithm.MCTS_frame_new.MCTS as MCT
import Poker_algorithm.MCTS_frame_new.preflop_combat as preflop_combat
import Poker_algorithm.MCTS_frame_new.flop_combat as flop_combat
import Poker_algorithm.MCTS_frame_new.turn_and_river_combat as turn_and_river_combat

'''
8.15注释：
这里将会简单的介绍一下下面的4*3个决策函数
p/f/t/r是四个阶段（pre/flop/turn/river 首字母
f/s/t是代表阶段内行为数
f是第一次，s是第二次，剩余行为均为t
参数统一：
cards           手牌
deck            己方视角牌库
our_model       己方模型
opp_model       对手模型
board_cards     场上上一轮的卡
add_card        此轮开始时场上翻出的卡
preflop_table   数据库
test_times      测试次数
返回值：返回行为，用于判断游戏进度
返回值会后期调整
'''
def pf(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    # preflop_pre
    aaset = preflop_combat.preflop_pre(cards, preflop_table)
    # action & amount set
    action = aaset[0]
    # 先手动作结束
    print("preflop_pre_action:" + str(action))
    if action == 0:
        return 0
        # 弃牌游戏结束
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
        our_model.action_status = 2
    our_model.action_set.append(action)  # 操作添加
    MCT.status_evaluation(our_model, opp_model)  # 状态评估刷新
    return action

def ps(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    #test_times:2000
    MCT.status_evaluation(opp_model, our_model)
    # 为什么要开始在每一个函数前评估对手行为状态？
    # 因为非EvE对战中对手的状态刷新是需要己方来完成的，不然会有大bug
    preflop_combat.refresh_preflop_for_post(opp_model, deck, preflop_table)
    aaset = preflop_combat.preflop_post(cards, preflop_table, opp_model, test_times)
    action = aaset[0]
    print("preflop_post_action: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    our_model.action_set.append(action)
    MCT.status_evaluation(our_model, opp_model)
    return action


def pt(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    #test_times:2000
    MCT.status_evaluation(opp_model, our_model)
    preflop_combat.refresh_preflop_for_post(opp_model, deck, preflop_table)
    # print(len(opp_model.possible_set))
    aaset = preflop_combat.preflop_afterward(cards, preflop_table, opp_model, test_times)
    action = aaset[0]
    print("preflop_pre_reaction: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
        MCT.status_evaluation(our_model, opp_model)
    our_model.action_set.append(action)
    return action



def ff(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    # test_times:50000
    MCT.status_evaluation(opp_model, our_model)
    flop_combat.refresh_preflop_for_pre(opp_model, our_model, deck, preflop_table)
    aaset = flop_combat.flop_pre(opp_model, deck, cards, board_cards, test_times)
    action = aaset[0]
    print("flop_first_action: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    our_model.action_set.append(action)
    MCT.status_evaluation(our_model, opp_model)
    return action

def fs(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    #test_times:10000
    MCT.status_evaluation(opp_model, our_model)
    preflop_combat.refresh_preflop_for_post(opp_model, deck, preflop_table)
    # print("refresh over!")
    aaset = flop_combat.flop_post(opp_model, cards, deck, board_cards, preflop_table, test_times)
    action = aaset[0]
    print("flop_second_action: " + str(action))
    our_model.action_set.append(action)
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    MCT.status_evaluation(our_model, opp_model)
    return action


def ft(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    #test_times:10000
    MCT.status_evaluation(opp_model, our_model)
    flop_combat.refresh_flop_for_post(opp_model, board_cards, preflop_table)
    aaset = flop_combat.flop_post(opp_model, cards, deck, board_cards, preflop_table, test_times)
    action = aaset[0]
    print("flop_pre_reaction: " + str(action))
    our_model.action_set.append(action)
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
        MCT.status_evaluation(our_model, opp_model)
    return action


def tf(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    MCT.status_evaluation(opp_model, our_model)
    turn_and_river_combat.refresh_flop_for_pre(opp_model, board_cards, add_card, preflop_table)
    # print(len(opp_model.possible_set))
    board_4_cards = board_cards + add_card
    aaset = turn_and_river_combat.turn_pre(opp_model, cards, board_4_cards, deck)
    action = aaset[0]
    print("turn_first_action: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    our_model.action_set.append(action)
    MCT.status_evaluation(our_model, opp_model)
    return action


def ts(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    MCT.status_evaluation(opp_model, our_model)
    turn_and_river_combat.refresh_rest(opp_model, board_cards, add_card)
    board_4_cards = board_cards + add_card
    aaset = turn_and_river_combat.turn_post(cards, deck, board_4_cards, opp_model)
    action = aaset[0]
    print("turn_second_action: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    our_model.action_set.append(action)
    MCT.status_evaluation(our_model, opp_model)
    return action


def tt(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    MCT.status_evaluation(opp_model, our_model)
    turn_and_river_combat.refresh_rest(opp_model, board_cards, add_card)
    board_4_cards = board_cards + add_card
    aaset = turn_and_river_combat.turn_post(cards, deck, board_4_cards, opp_model)
    action = aaset[0]
    print("turn_pre_reaction: " + str(action))
    our_model.action_set.append(action)
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
        MCT.status_evaluation(our_model, opp_model)
    return action


def rf(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    MCT.status_evaluation(opp_model, our_model)
    turn_and_river_combat.refresh_rest(opp_model, board_cards, add_card)
    board_5_cards = board_cards + add_card
    aaset = turn_and_river_combat.river_pre(cards, board_5_cards, opp_model)
    action = aaset[0]
    print("river_first_action: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    our_model.action_set.append(action)
    MCT.status_evaluation(our_model, opp_model)
    return action


def rs(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    MCT.status_evaluation(opp_model, our_model)
    turn_and_river_combat.refresh_rest(opp_model, board_cards, add_card)
    board_5_cards = board_cards + add_card
    aaset = turn_and_river_combat.river_post(cards, board_5_cards, opp_model)
    action = aaset[0]
    print("river_second_action: " + str(action))
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
    our_model.action_set.append(action)
    MCT.status_evaluation(our_model, opp_model)
    return action

def rt(cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table, test_times):
    MCT.status_evaluation(opp_model, our_model)
    turn_and_river_combat.refresh_rest(opp_model, board_cards, add_card)
    board_5_cards = board_cards + add_card
    aaset = turn_and_river_combat.river_post(cards, board_5_cards, opp_model)
    action = aaset[0]
    print("river_reaction: " + str(action))
    our_model.action_set.append(action)
    if action == 0:
        return 0
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        our_model.bet_amount.append(aaset[1])
        MCT.status_evaluation(our_model, opp_model)
    return action

def make_action(our_model, opp_model):
    print("make your action: \n"
          "0 for giving up\n"
          "1 for follow\n"
          "2 for raise")
    choice = int(input())
    if choice == 1:
        our_model.action_set.append(1)
    elif choice == 2:
        our_model.action_set.append(2)
    MCT.status_evaluation(our_model, opp_model)
    return choice

class Game:
    def __init__(self):
        self.round = 1 # 1,2,3,4代表阶段
        self.counter = 1
        self.deck = [] # 公共牌库（测试用，前后端链接不需要）
        self.board_cards = []
        self.add_card = []
        self.act_num = 1 # 和counter的区别：counter是一个阶段的行为编号，act_num是全局的行动数
        self.bet_amount = 15 # 15是大小盲注和，可能会根据前端设置接口
        self.set_amount = 10

def action_choice(game, cards, deck, our_model, opp_model, board_cards, add_card ,preflop_table):
    '''
    :param game: game类
    :param cards: 进行行为的玩家手牌
    :param deck: 进行行为的玩家
    :param our_model: 己方模型，访问内容：己方行为
    :param opp_model: 对手模型，访问内容：模型内牌型分布，对手决策状态，对手决策历史
    :param board_cards: 场上原本的卡，对应length为：p-0；f-3；t-3；r-4
    :param add_card: 新翻开的卡（flop阶段因为函数的特殊性所以把三张公共牌视为原本的卡
                        对应length为：p-0；f-0；t-1；r-1  长度为0时传任意参数不会调用
    :param preflop_table: 在p和f阶段调用的数据库
    # :param test_times: 测试次数，在p和f阶段调用，t和r次数已经内置好，当然可以通过重构使其包含此参数
    :return: 任意需求的接口
    '''
    x = 0
    test_times = 0
    game.act_num += 1
    if game.round == 1:
        if game.counter == 1:
            x = pf(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)
        if game.counter == 2:
            x = ps(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, 2000)
            if x == 1 or 2: # 补齐小盲注
                game.bet_amount += 0.5 * game.set_amount
                our_model.chips -= 0.5 * game.set_amount
        if game.counter >= 3:
            x = pt(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, 2000)
    if game.round == 2:
        if game.counter == 1:
            x = ff(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, 50000)
        if game.counter == 2:
            x = fs(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, 10000)
        if game.counter >= 3:
            x = ft(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, 10000)
    if game.round == 3:
        if game.counter == 1:
            x = tf(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)
        if game.counter == 2:
            x = ts(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)
        if game.counter >= 3:
            x = tt(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)
    if game.round == 4:
        if game.counter == 1:
            x = rf(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)
        if game.counter == 2:
            x = rs(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)

        if game.counter >= 3:
            x = rt(cards, deck, our_model, opp_model, board_cards, add_card, preflop_table, test_times)

                # 游戏结束
    if x == 2:
        game.counter += 1
    elif x == 1 and game.counter >= 2:
        game.round += 1
        game.counter = 1
    else:
        game.counter += 1
    return x



