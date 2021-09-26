from Poker_algorithm.EHS_compare import Analysis_class as An
from Poker_algorithm.EHS_compare import compare_func as com
import random


class Forecaster():
    def __init__(self,my_cards,board_cards,simulate_times):
        self.my_cards = my_cards
        self.board_cards = board_cards
        self._type = [0]*10
        self.simulate_times = simulate_times
        a = self.HP()

        self.p_pot = a[0]
        self.n_pot = a[1]
        self.hand_strength = a[2]

        self.winning_p = self.hand_strength*(1-self.n_pot)+(1-self.hand_strength)*self.p_pot
        self.type = [x/self.simulate_times for x in self._type]

    def HP(self):
        cards = [_ for _ in range(52)]
        known_cards = self.my_cards + self.board_cards
        for _ in known_cards:
            cards.remove(_)
        hp = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # [ahead, tied, behind]
        hp_total = [0] * 3

        test = [0] * 3

        # enumerate all of the opponent hands
        for i in range(self.simulate_times):
            random.shuffle(cards)
            opp_cards = [cards[-1], cards[-2]]
            judge = com.Judgement(self.my_cards, opp_cards, self.board_cards)
            board_cards2 = self.board_cards + [cards[-3], cards[-4]]
            judge_2 = com.Judgement(self.my_cards, opp_cards, board_cards2)
            self._type[judge_2.type] += 1

            o = judge.status
            l = judge_2.status
            hp[o][l] += 1
            hp_total[judge.status] += 1
            test[l] += 1

        divis1 = (hp_total[2] + hp_total[1] / 2)
        divis2 = (hp_total[0] + hp_total[1] / 2)
        if divis1 != 0:
            p_pot = (hp[2][0] + hp[2][1] / 2 + hp[1][0] / 2) / divis1
        else:
            p_pot = 1
        if divis2 != 0:
            n_pot = (hp[0][2] + hp[1][2] / 2 + hp[0][1] / 2) / divis2
        else:
            n_pot = 1
        hand_strength = (hp_total[0] + hp_total[1] / 2) / sum(hp_total)
        for i in range(10):
            self._type[i] = self._type[i]/self.simulate_times
        return p_pot, n_pot, hand_strength, self._type

