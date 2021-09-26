import random
import Poker_algorithm.MCTS_frame_new.MCTS as MCT
import Poker_algorithm.MCTS_frame_new.preflop_data as preflopdata
import Poker_algorithm.MCTS_frame_new.preflop_combat as preflop_combat
import Poker_algorithm.MCTS_frame_new.flop_combat as flop_combat
import Poker_algorithm.MCTS_frame_new.turn_and_river_combat as turn_and_river_combat


for time in range(20):
    preflop_table = preflopdata.get_table()
    pre_player = MCT.Opponent_Model()
    post_player = MCT.Opponent_Model()
    # pre_player: player1 模型；  post_player: player2 模型
    # 初始化对手模型以及数据库

    deck = [i for i in range(52)]
    actual_deck = list(deck)
    '''actual_deck为真实牌库，模拟对局用，算法中不会用到'''
    pre_cards = random.sample(deck,2)
    print("pre_cards:  "+str(pre_cards))
    for x in pre_cards:
        actual_deck.remove(x)
    pre_deck = list(actual_deck) # 先手视角的牌库
    post_cards = random.sample(actual_deck,2)
    print("post_cards:  "+str(post_cards))
    for x in post_cards:
        actual_deck.remove(x)
        deck.remove(x)
    post_deck = list(deck)      # 后手视角的Paiute
    # 测试起牌准备工作完毕

    '''
    preflop 阶段模拟博弈
    '''

    action = preflop_combat.preflop_pre(pre_cards, preflop_table)
    # 先手动作结束
    print("preflop_pre_action:" + str(action))
    if action == 0:
        print("\n\n\n")
        continue
        # 弃牌游戏结束
    pre_player.action_set.append(action)
    post_action = preflop_combat.preflop_post(post_cards, preflop_table, pre_player, 200)
    print("preflop_post_action: " + str(post_action))
    if post_action == 0:
        print("\n\n\n")
        continue
        # 弃牌游戏结束
    post_player.action_set.append(post_action)
    print(" ")

    '''
    flop 阶段模拟博弈
    '''
    #准备阶段
    board_cards = random.sample(actual_deck,3)
    for card in board_cards:
        actual_deck.remove(card)
        pre_deck.remove(card)
        post_deck.remove(card)
    print("board_cards: "+str(board_cards))
    #结束
    #传参：
    """
    preflop_for_pre && flop_pre: 对手模型，己方模型，己方视角牌库，table,(flop_pre还有己方手牌
    preflop_for_post && flop_post: 对手模型，table， 己方视角牌库
    """
    #flop_combat.refresh_preflop_for_pre(post_player, pre_player, pre_deck, preflop_table)
    #flop_combat.refresh_preflop_for_post(pre_player, post_deck, preflop_table)
    #print(len(pre_player.possible_set))
    #print(len(post_player.possible_set))
    # possible_set是一个手牌合集，根据权重的不同，不同手牌可能会重复若干次（至少一次
    # action为跟注时方差较小，action为加注时方差较大，且整体偏向较大的牌力
    # 分布规则是由preflop行为规则进行数学推算得出的，几个代码的常数为统一系统，不能轻易修改
    # 双方视角下现在的对手模型已经改变，基于改变后的模型进行进一步决策，上面的两个函数已经封装到决策函数内
    action = flop_combat.flop_pre(post_player, pre_player, pre_deck, preflop_table, board_cards, pre_cards, 50000)
    pre_player.action_set.append(action)
    print("flop_pre_action: "+str(action))
    print("pre_action_set: "+str(pre_player.action_set))
    if action==0:
        print("\n\n\n")
        continue
    action = flop_combat.flop_post(pre_player, post_cards, post_deck, board_cards, preflop_table, 10000)
    print("flop_post_action: "+ str(action))
    post_player.action_set.append(action)
    if action == 0:
        print("\n\n\n")
        continue
    '''
    turn 阶段模拟博弈
    '''
    # 准备阶段
    turn_card = random.sample(actual_deck, 1)
    for card in turn_card:
        actual_deck.remove(card)
        pre_deck.remove(card)
        post_deck.remove(card)
    board_4_cards = board_cards + turn_card
    print("board_cards: " + str(board_4_cards))
    # 结束
    turn_and_river_combat.refresh_flop_for_pre(post_player, board_cards, preflop_table)
    print("\n\n\n")
    """
    7.14 问题出现：
    1. 单回合加注后跟进的状态刷新没有解决，如单回合存在加注后的决策以及对手模型是否刷新的决策
    2. 函数封装的问题，因为没有将刷新自己的行为模型写入函数中，所以在封装时要在新函数中添加这一步
    在此做一下记录
    3. post和pre在对手同样操作次数时暂时用的是同一个判断框架，但可能判断保守程度会有所区别
    此外，如对手在flop阶段加注，虽然己方仍在flop阶段，但实行的决策可能和turn阶段以及river阶段
    属于同一种模式。这个有待解决
    """