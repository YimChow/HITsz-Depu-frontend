from Poker_algorithm.EHS_compare import Analysis_class as An


class Judgement:
    def __init__(self, our_cards, opp_cards, board_cards):
        # 可访问属性
        self.type = -1
        self.status = -1    # ahead:0 tied:1 behind:2
        self.opp_type = -1

        self._our_cards = our_cards  # 手牌
        self._opp_cards = opp_cards  # 对手手牌
        self._board_cards = board_cards
        self.compare()

    def compare(self):
        my_analyst = An.Analysis(self._our_cards + self._board_cards)  # 将自己的牌型分析结果存储
        self.type = my_analyst.type()                                  # 牌型类别
        my_score = (10 - self.type)*3000 + my_analyst.judge[self.type]  # 牌力值

        opp_analyst = An.Analysis(self._opp_cards + self._board_cards)
        self.opp_type = opp_analyst.type()
        opp_score = (10 - self.opp_type) *3000 + opp_analyst.judge[self.opp_type]

        if my_score > opp_score:
            self.status = 0                         # ahead
            return
        elif my_score < opp_score:
            self.status = 2                         # behind
            return
        else:   # my_score == opp_score（对tied的情况不足的补充）

            if self.type == 4:
                # print("hahahahahanomay!")
                my_flush_cards = sorted(my_analyst.flush_cards, reverse=True)
                rival_flush_cards = sorted(opp_analyst.flush_cards, reverse=True) # 比较同花高牌
                if my_flush_cards > rival_flush_cards:
                    self.status = 0
                    return
                elif my_flush_cards == rival_flush_cards:
                    self.status = 1
                    return
                else:
                    self.status = 2
                    return

            """            
            if self.type == 6:
                my_two_cards = my_analyst.two_high_cards
                rival_two_cards = opp_analyst.two_high_cards
                if my_two_cards > rival_two_cards:
                    self.status = 0
                    return
                elif my_two_cards == rival_two_cards:
                    self.status = 1
                    return
                else:
                    self.status = 2
                    return
            """
            if self.type == 8:
                my_three_cards = my_analyst.three_cards_in_pairs
                rival_three_cards = opp_analyst.three_cards_in_pairs  # 另外三个高牌
                if my_three_cards > rival_three_cards:
                    self.status = 0
                    return
                elif my_three_cards == rival_three_cards:
                    self.status = 1
                    return
                else:
                    self.status = 2
                    return

            elif self.type == 9:
                m_h = my_analyst.high_cards
                o_h = opp_analyst.high_cards
                # print(my_analyst.high_cards,opp_analyst.high_cards)
                if m_h > o_h:
                    self.status = 0
                    return
                elif m_h == o_h:
                    self.status = 1
                    return
                else:
                    self.status = 2
                    return
            else:
                self.status = 1     # 对不起这里可以运行到…… （什么条件下可以运行到？questioned by aloka(俩人牌等价？by Eve
                # print("lookhere!!!")
                return



if __name__ == "__main__":
    a = Judgement([50,41],[37,3],[34,9,7,11,12])
    print(a.opp_type)
    print(a.status)





