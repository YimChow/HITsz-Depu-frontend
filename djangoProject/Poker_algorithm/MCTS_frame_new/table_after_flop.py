import random
import Poker_algorithm.FuncToUse.FuncInstruction as func
import Poker_algorithm.MCTS_frame_new.preflop_data as preflop_data

def new_table(board_cards, test_times):
    """
    :param board_cards: 公共牌（3-5张）
    :param test_times: 抽样次数
    :return:  公共牌对应的flop牌力
    """
    table = [[0]*52 for m in range(52)]
    deck = [i for i in range(52)]
    length = len(board_cards)
    '''
    7.12 对算法逻辑的几个说明
    1. table的构建思路：
    将table进行排序，根据大小的分布重新映射到prefloptable的分布数值（方差减小）
    间接形成了新的估值函数，然后根据强弱变化进行对手模型筛选以及自我的决策
    2. 该函数的部分说明，下面两个初始的空列表分别存储牌型依旧对应的牌力
    有点类似结构体但是我比较懒，因为这一部分复杂度相比之前的可以忽略所以就不考虑排序浪费的时间了
    第一部分是排序部分，第二部分是映射存储到table的部分
    3. 其他说明：
        3.1 length是一个伏笔，根据length不同可以依照同样的逻辑实现四张公共牌和五张公共牌对应的新table
        3.2 为什么要进行映射：
            对于真实的牌力以及自己的强弱估计时，场上三张牌起到的决定因素甚至大于自己的手牌
            例如：如果发了三个A，那场上牌力基本上决定了整个对局的平均牌力[最低1111，最高1995，十次抽样就可保证差异较小]
            如果按照原来的框架会出现无脑加注的情况，此时应该将已知数据变为3张牌进行重新的抽样估计
            ### 四张公共牌和五张公共牌甚至可以考虑枚举，因为筛选后对手的模型变小而且抽样的循环轮数也减少了很多    
    '''
    counter = 0
    sort_set = []
    sort_strength = []
    for card in board_cards:
        deck.remove(card)
    if length == 3:
        for i in deck:
            for j in deck:
                if i == j : continue
                counter += 1
                temp_deck = list(deck)
                our_cards = [i,j]
                temp_deck.remove(i)
                temp_deck.remove(j)
                card_strength = 0
                for k in range(test_times):
                    two_cards = random.sample(temp_deck,2)
                    card_strength += func.get_cards_score(our_cards, board_cards+two_cards)
                card_strength /= (test_times*10)
                if counter == 1:
                    sort_set.append([i,j])
                    sort_strength.append(card_strength)
                else:
                    index = 0
                    for p in sort_strength:
                        if p > card_strength:
                            index += 1
                    #print(our_cards)
                    sort_set.insert(index,our_cards)
                    #print(sort_set[0],end="  ")
                    sort_strength.insert(index,card_strength)
        #print(sort_strength)
        #print(len(sort_set))
        #print(sort_set)
        #print(len(sort_strength))          #all for test
        """
        然后是激动人心的映射环节！
        之前构建preflop_table的伏笔回收！按照比例来映射
        五分一段表创建后根据分布来直接按比例来重新赋值
        """
        distribution = list(get_set())
        for i in range(57): # 57: 650-930有57种牌值
            a = distribution[i]
            distribution[i] = int(a*2352)
        index = 0
        for i in range(2352):
            while i > distribution[index]:
                index += 1
            hands = sort_set[2351-i]
            #print(hands)  #for test
            card1 = hands[0]
            card2 = hands[1]
            table[card1][card2] = 650 + index*5
        #print(table[0][1])
        return table

    if length == 4:
        for i in deck:
            for j in deck:
                if i == j: continue
                counter += 1
                temp_deck = list(deck)
                score= 0
                for card in temp_deck:
                    rivercard = [card]
                    # 单起一张牌
                    hand_cards = [i,j]
                    score += func.get_cards_score(hand_cards, board_cards+rivercard)
                score /= 460
                if counter == 1:
                    # 边界情况单独处理
                    sort_set.append([i,j])
                    sort_strength.append(score)
                else:
                    index = 0

                    for p in sort_strength:
                        if p > score:
                            index += 1
                    #print(our_cards)
                    sort_set.insert(index,[i,j])
                    #print(sort_set[0],end="  ")
                    sort_strength.insert(index,score)
        distribution = list(get_set())

        for i in range(57):
            a = distribution[i]
            distribution[i] = int(a * 2256)
        index = 0
        for i in range(2256):
            while i > distribution[index]:
                index += 1
            hands = sort_set[2255 - i]
            # print(hands)  #for test
            card1 = hands[0]
            card2 = hands[1]
            table[card1][card2] = 650 + index * 5
        return table


    if length == 5:
        for i in deck:
            for j in deck:
                if i == j:
                    continue
                hand_cards = [i,j]
                counter += 1
                temp_deck = list(deck)
                score = func.get_cards_score(hand_cards, board_cards)
                if counter == 1:
                    # 边界情况单独处理
                    sort_set.append([i,j])
                    sort_strength.append(score)
                else:
                    index = 0

                    for p in sort_strength:
                        if p > score:
                            index += 1
                    #print(our_cards)
                    sort_set.insert(index,[i,j])
                    #print(sort_set[0],end="  ")
                    sort_strength.insert(index,score)
        distribution = list(get_set())
        for i in range(57):
            a = distribution[i]
            distribution[i] = int(a * 2162)
        index = 0
        for i in range(2162):
            while i > distribution[index]:
                index += 1
            hands = sort_set[2161 - i]
            # print(hands)  #for test
            card1 = hands[0]
            card2 = hands[1]
            table[card1][card2] = 650 + index * 5
        return table






def get_set():
    # 获取五分一段表的分布比例
    prefloptable = preflop_data.get_table()
    set = [0]*57
    for i in range(51):
        for j in range(i+1, 52):
            x = prefloptable[i][j]
            p = int ((x - 650)/5)
            set[p]+=1
    q = sum(set)
    for i in range(57):
        set[i] /= q
        if i > 0:
            set[i] += set[i-1]
    return set


if __name__ == "__main__":
    deck = [i for i in range(52)]
    board_card = random.sample(deck,5)
    print(board_card)
    board_card = [33,37,41,20,16]
    '''精确度初步分析'''
    new_table(board_card,1)

