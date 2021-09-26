import random

import Poker_algorithm.FuncToUse.FuncInstruction as Func
file_name = "preflop_table3.txt"
with open(file_name, "w") as f:
    deck = [x for x in range(52)]
    print(deck)
    card1 = 0
    card2 = 0
    counter = 169
    preflop_table = [[0]*13]*13
    for i in range(13):
        for j in range(13):
            if i >= j:
                card1 = 4*i
                card2 = 4*j+1
            if i < j :
                card1 = 4*i
                card2 = 4*j
            cards = [card1, card2]
            this_deck = list(deck)
            this_deck.remove(card1)
            this_deck.remove(card2)
            # 将13*13的数据分别抽样估值
            a = 0
            for n in range(20000):
                board_cards = random.sample(this_deck, 5)
                a += Func.get_cards_score(cards,board_cards)
            a = int(a/200000)
            preflop_table[i][j] = a
            f.write(str(a) + "\t")
            counter-=1
            print(counter)
        f.write("\n")

        
