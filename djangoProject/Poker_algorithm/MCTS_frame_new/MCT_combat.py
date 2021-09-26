import random
import Poker_algorithm.MCTS_frame_new.MCTS as MCT
import Poker_algorithm.MCTS_frame_new.preflop_data as preflopdata
import Poker_algorithm.MCTS_frame_new.preflop_combat as preflop_combat
import Poker_algorithm.MCTS_frame_new.flop_combat as flop_combat
import Poker_algorithm.MCTS_frame_new.turn_and_river_combat as turn_and_river_combat
import Poker_algorithm.EHS_compare.compare_func as cmp \
# import action_packages as ap

'''
说明：
MCTcombat
是模拟对局流程的文件，里面有模拟发牌，决策显示等功能
主要用于直观上的测试
可以较为清晰的判断决策的合理性
更为清晰的函数调用指引见
Combat_Func_to_use.py
置顶：重构后原则：每次决策前刷新对手状态
'''
if __name__ == "__main__":
    preflop_table = preflopdata.get_table()
    pre_player = MCT.Opponent_Model()
    pre_player.bet_amount.append(0.5)
    post_player = MCT.Opponent_Model()
    post_player.bet_amount.append(1)
    model_set = [pre_player,post_player]
    # pre_player: player1 模型；  post_player: player2 模型
    # 初始化对手模型以及数据库

    deck = [i for i in range(52)]
    actual_deck = list(deck)
    '''actual_deck为真实牌库，模拟对局用，算法中不会用到'''
    pre_cards = random.sample(deck,2)
    print("pre_cards:  "+str(pre_cards),end=" ")
    MCT.cards_visualize(pre_cards)
    for x in pre_cards:
        actual_deck.remove(x)
    pre_deck = list(actual_deck) # 先手视角的牌库
    post_cards = random.sample(actual_deck,2)
    print("post_cards:  "+str(post_cards),end=" ")
    MCT.cards_visualize(post_cards)
    for x in post_cards:
        actual_deck.remove(x)
        deck.remove(x)
    post_deck = list(deck)      # 后手视角的Paiute
    # 测试起牌准备工作完毕



    '''
    preflop 阶段模拟博弈
    '''
    # preflop_pre
    aaset = preflop_combat.preflop_pre(pre_cards, preflop_table)
    # action & amount set
    action = aaset[0]
    # 先手动作结束
    print("preflop_pre_action:" + str(action))
    if action == 0:
        exit(0)
        # 弃牌游戏结束
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        pre_player.bet_amount.append(aaset[1])
        pre_player.action_status = 2
    pre_player.action_set.append(action) # 操作添加
    MCT.status_evaluation(pre_player, post_player)  # 状态评估刷新
    # preflop_post
    preflop_combat.refresh_preflop_for_post(pre_player, post_deck, preflop_table)
    aaset = preflop_combat.preflop_post(post_cards, preflop_table, pre_player, 2000)
    action = aaset[0]
    print("preflop_post_action: " + str(action))
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: "+ str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    post_player.action_set.append(action)
    MCT.status_evaluation(post_player, pre_player)
    #print(len(pre_player.possible_set))
    counter = 1
    # 奇偶操作不同
    # 引入counter， counter若是奇数则先手操作，若为偶数则为后手操作
    while(action == 2):
        if counter%2 == 1:
            preflop_combat.refresh_preflop_for_post(post_player, pre_deck, preflop_table)
            #print(len(post_player.possible_set))
            aaset = preflop_combat.preflop_afterward(pre_cards, preflop_table, post_player, 2000)
            action = aaset[0]
            print("preflop_pre_reaction: " + str(action))
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                pre_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(pre_player, post_player)
            pre_player.action_set.append(action)

        else:
            #preflop_combat.refresh_preflop_for_post(pre_player, post_deck, preflop_table)
            aaset = preflop_combat.preflop_afterward(post_cards, preflop_table, pre_player, 2000)
            action = aaset[0]
            print("preflop_post_reaction: " + str(action))
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                post_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(post_player, pre_player)
            post_player.action_set.append(action)
        counter += 1


    #print(len(pre_player.possible_set))
    #print(len(post_player.possible_set))

    # 添加了过渡函数
    print(" ")
    MCT.next_phace(model_set)

    '''
    flop 阶段模拟博弈
    '''
    #准备阶段
    #
    # 注意counter的问题， 角色会进行对调
    #

    def switch_player(a,b,counter,c,d,e,f):
        if counter%2 == 0:
            return b,a,d,c,f,e
        else: return a,b,c,d,e,f

    pre_player, post_player, pre_cards, post_cards, pre_deck, post_deck = \
        switch_player(pre_player, post_player,counter, pre_cards, post_cards, pre_deck, post_deck)

    print("flop start: the action set are:")
    print(pre_player.action_set)
    print(post_player.action_set)

    board_cards = random.sample(actual_deck,3)
    #board_cards = [48,49,40]
    for card in board_cards:
        actual_deck.remove(card)
        pre_deck.remove(card)
        post_deck.remove(card)
    print("board_cards: "+str(board_cards),end=" ")
    MCT.cards_visualize(board_cards)
    #print("deck lenth "+str(len(pre_deck))+" "+str(len(post_deck)))
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
    flop_combat.refresh_preflop_for_pre(post_player,pre_player,pre_deck,preflop_table)
    print("refresh over")
    aaset = flop_combat.flop_pre(post_player, pre_deck, board_cards, pre_cards, 50000)
    action = aaset[0]
    print("flop_first_action: "+str(action))
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    pre_player.action_set.append(action)
    MCT.status_evaluation(pre_player, post_player)
    #print("pre_action_set: "+str(pre_player.action_set))
    #preflop_pre结束
    #preflop_post阶段

    preflop_combat.refresh_preflop_for_post(pre_player, post_deck, preflop_table)
    #print("refresh over!")
    aaset = flop_combat.flop_post(pre_player, post_cards, post_deck, board_cards, preflop_table, 10000)
    '''mark'''
    action = aaset[0]
    print("flop_second_action: "+ str(action))
    post_player.action_set.append(action)
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    MCT.status_evaluation(post_player, pre_player)
    # 进入持续加注阶段
    counter = 1
    while action == 2:
        if counter % 2 == 1 :
            flop_combat.refresh_flop_for_post(post_player, board_cards, preflop_table)
            aaset = flop_combat.flop_post(post_player, pre_cards, pre_deck, board_cards, preflop_table, 10000)
            action = aaset[0]
            print("flop_pre_reaction: " + str(action))
            pre_player.action_set.append(action)
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                pre_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(pre_player, post_player)
        else:
            flop_combat.refresh_flop_for_post(pre_player, board_cards, preflop_table)
            aaset = flop_combat.flop_post(pre_player, post_cards, post_deck, board_cards, preflop_table, 10000)
            action = aaset[0]
            print("flop_post_reaction: " + str(action))
            post_player.action_set.append(action)
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                post_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(post_player, pre_player)
                # 8.2优化：只有在额外加注的情况才重新刷新对手的决策状态

        counter += 1



    pre_player, post_player, pre_cards, post_cards, pre_deck, post_deck = \
        switch_player(pre_player, post_player,counter, pre_cards, post_cards, pre_deck, post_deck)


    # 持续加注结束

    '''
    turn 阶段模拟博弈
    '''
    # 准备阶段
    MCT.next_phace(model_set)
    print("turn start: the action set are:")
    print(pre_player.action_set)
    print(post_player.action_set)


    turn_card = random.sample(actual_deck,1)
    for card in turn_card:
        actual_deck.remove(card)
        pre_deck.remove(card)
        post_deck.remove(card)
    board_4_cards = board_cards + turn_card
    print("board_cards: "+str(board_4_cards),end=" ")
    MCT.cards_visualize(board_4_cards)
    # 结束
    turn_and_river_combat.refresh_flop_for_pre(post_player, board_cards, turn_card, preflop_table)
    #print(len(post_player.possible_set))
    aaset = turn_and_river_combat.turn_pre(post_player, pre_cards, board_4_cards,
                                   pre_deck)
    action = aaset[0]
    print("turn_first_action: "+str(action))
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    pre_player.action_set.append(action)
    MCT.status_evaluation(pre_player, post_player)
    turn_and_river_combat.refresh_rest(pre_player, board_cards, turn_card)
    aaset = turn_and_river_combat.turn_post(post_cards, post_deck , board_4_cards, pre_player)
    action = aaset[0]
    print("turn_second_action: "+str(action))
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    post_player.action_set.append(action)
    MCT.status_evaluation(post_player, pre_player)
    # length not suited, error!
    # 进入持续加注阶段
    counter = 1
    while action == 2:
        if counter % 2 == 1 :
            turn_and_river_combat.refresh_rest(post_player, board_cards, turn_card)
            aaset = turn_and_river_combat.turn_post(pre_cards, pre_deck, board_4_cards, post_player)
            action = aaset[0]
            print("turn_pre_reaction: " + str(action))
            pre_player.action_set.append(action)
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                pre_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(pre_player, post_player)
        else:
            turn_and_river_combat.refresh_rest(pre_player, board_cards, turn_card)
            aaset = turn_and_river_combat.turn_post(post_cards, post_deck, board_4_cards, pre_player)
            action = aaset[0]
            print("turn_post_reaction: " + str(action))
            post_player.action_set.append(action)
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                post_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(post_player, pre_player)
        counter += 1


    pre_player, post_player, pre_cards, post_cards, pre_deck, post_deck = \
        switch_player(pre_player, post_player,counter, pre_cards, post_cards, pre_deck, post_deck)


    MCT.next_phace(model_set)
    print("river start: the action set are:")
    print(pre_player.action_set)
    print(post_player.action_set)
    river_card = random.sample(actual_deck,1)
    for card in river_card:
        actual_deck.remove(card)
        pre_deck.remove(card)
        post_deck.remove(card)
    board_5_cards = board_4_cards + river_card
    print("board_cards: "+str(board_5_cards),end=" ")
    MCT.cards_visualize(board_5_cards)
    # river 准备结束
    # river 的刷新模型模式和turn基本一致，但没有先后手差异，先手用3->4刷新，后手用4->5刷新

    turn_and_river_combat.refresh_rest(post_player, board_4_cards, river_card)
    aaset = turn_and_river_combat.river_pre(pre_cards, board_5_cards, post_player)
    action = aaset[0]
    print("river_first_action: "+str(action))
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    pre_player.action_set.append(action)
    MCT.status_evaluation(pre_player, post_player)

    turn_and_river_combat.refresh_rest(pre_player, board_4_cards, river_card)
    aaset = turn_and_river_combat.river_post(post_cards, board_5_cards, pre_player)
    action = aaset[0]
    print("river_second_action: "+str(action))
    if action == 0:
        exit(0)
    if action == 2:
        print("raise_amount: " + str(aaset[1]))
        post_player.bet_amount.append(aaset[1])
    post_player.action_set.append(action)
    MCT.status_evaluation(post_player, pre_player)
    while action == 2:
        if counter % 2 == 1 :
            turn_and_river_combat.refresh_rest(post_player, board_4_cards, river_card)
            aaset = turn_and_river_combat.river_post(pre_cards, board_5_cards, post_player)
            action = aaset[0]
            print("turn_pre_reaction: " + str(action))
            pre_player.action_set.append(action)
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                pre_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(pre_player, post_player)
        else:
            turn_and_river_combat.refresh_rest(pre_player, board_4_cards, river_card)
            aaset = turn_and_river_combat.river_post(post_cards, board_5_cards, pre_player)
            action = aaset[0]
            print("turn_post_reaction: " + str(action))
            post_player.action_set.append(action)
            if action == 0:
                exit(0)
            if action == 2:
                print("raise_amount: " + str(aaset[1]))
                post_player.bet_amount.append(aaset[1])
                MCT.status_evaluation(post_player, pre_player)
        counter += 1
    # 游戏结束
    judge = cmp.Judgement(pre_cards, post_cards, board_cards)
    if judge.status == 0:
        print("pre_player_wins!")
    if judge.status == 1:
        print("draw!")
    else:
        print("post_player_wins!")
    print("pre: action and amount set:"+str(pre_player.action_set)+"\n"+str(pre_player.bet_amount))
    print("post: action and amount set:"+str(post_player.action_set)+"\n"+str(post_player.bet_amount))


    """
    8.10 关于持续加注阶段模型是否刷新进行思考：
    对已知信息利用不够充分
    """
