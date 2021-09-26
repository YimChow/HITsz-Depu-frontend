class Analysis:
    def __init__(self, test_cards):
        self.test_cards = test_cards        # 可以是五、六或七张噢
        self.fc = [0]*13                    # 牌值存储器
        self.st = [0]*4                     # 花色存储器
        self.sorted_cards = sorted(self.test_cards, reverse=True)
        self.three_cards_in_pairs = []      # 一对牌型存储三张杂牌
        self.high_cards = []                # 高牌降序存储五张牌
        self.two_high_cards = []             # 三条的两张杂牌
        self.flush_cards = []

        for x in self.test_cards:
            self.fc[x // 4] += 1
            self.st[x % 4] += 1

        self.judge = [0]*10

    def straight(self):
        """适用5，6，7张牌"""
        for i in range(9):
            if self.fc[12-i] != 0 and self.fc[11-i] != 0 and self.fc[10-i] != 0 and self.fc[9-i] != 0 and self.fc[8-i] != 0:
                # print(self.fc,13-i)
                self.judge[5] = 169*(13-i)        # 确保连牌之间可以比较大小
                return 5
        if self.fc[0] != 0 and self.fc[1] != 0 and self.fc[2] != 0 and self.fc[3]!=0 and self.fc[12]!=0:
            self.judge[5] = 169*4
            return 5
        return False

    def four_of_a_kind(self):
        """适用5，6，7"""
        for i in range(13):
            if self.fc[i] == 4:
                for j in range(12, -1, -1):
                    if self.fc[j] != 4 and self.fc[j] != 0:
                        self.judge[2] = (i+1) * 169 + (j+1)*13
                        return True
        return False

    def full_house(self):
        """葫芦和三条，5，6，7"""
        for i in range(12, -1, -1):
            a = 0
            if self.fc[i] == 3:
                for k in range(12, -1, -1):
                    if k != i:
                        if self.fc[k] == 2 or self.fc[k] == 3:  # 修复了两个三条不能判成葫芦的漏洞
                            self.judge[3] = (i + 1) * 169+ k*13
                            return 3
                        if a < 2 and self.fc[k] == 1:
                            self.two_high_cards.append(k)   # 三条同分判断：比较前两张高牌
                            a += 1
                self.judge[6] = (i + 1)*169+(1+self.two_high_cards[0])*13+self.two_high_cards[1]
                return 6
        return 0

    def flush(self):
        for i in range(4):
            if self.st[i] >= 5:
                for k in range(len(self.test_cards)):
                    if self.sorted_cards[k] % 4 == i:
                        self.two_high_cards.append(self.sorted_cards[k]//4)
                        self.flush_cards = self.two_high_cards[0:5]  # 存储同花当中的最高两张牌
                self.judge[4] = (self.two_high_cards[0] + 1)*169+(self.two_high_cards[1])*13
                return True
        return False

    def pairs(self):
        """同牌型比较时需调用牌值，5，6，7"""
        for i in range(12, -1, -1):
            if self.fc[i] == 2:
                for k in range(12,-1,-1):
                    if k != i and self.fc[k] == 2:
                        for h in range(12, -1, -1):
                            mark = self.fc[h]
                            if h != i and h != k and (mark == 1 or mark == 2):
                                self.judge[7] = 169*(i+1) + 13 * (k+1) + h  # i,j,k：第一第二大对和第一大单牌
                                return 7
                self.judge[8] = (i+1)*13*13  # 一对
                n = 0
                for r in range(12, -1, -1):
                    if self.fc[r] == 1:
                        n += 1
                        self.three_cards_in_pairs.append(r)
                    if n == 3:
                        return 8
        return False

    def royal_straight_flush(self):
        """五、六、七张牌版本"""
        for i in range(4):
            sets = {51 - i, 47 - i, 43 - i, 39 - i, 35 - i}
            if sets.issubset(self.sorted_cards):
                self.judge[0] = 169
                return 2
        for j in range(3):
            head = self.sorted_cards[j]
            sets = {head, head - 4, head - 8, head - 12, head - 16}
            if sets.issubset(self.sorted_cards):
                self.judge[1] = (head // 4 + 1)*169
                return 1
        for k in range(4):
            sets={0+k,48+k,4+k,8+k,12+k}
            if sets.issubset(self.sorted_cards):
                self.judge[1] = 4*169
                return 1
        return False

    def type(self):
        """返回牌型"""
        flag1 = self.royal_straight_flush()
        if flag1 == 2:
            return 0
        elif flag1 == 1:
            return 1
        elif self.four_of_a_kind():
            return 2
        else:
            flag2 = self.full_house()
            if flag2 == 3:
                return 3
            elif self.flush():
                return 4
            elif self.straight() == 5:
                return 5
            elif flag2 == 6:
                return 6
            else:
                flag3 = self.pairs()
                if flag3 == 7:
                    return 7
                elif flag3 == 8:
                    return 8
        self.high_cards = self.sorted_cards[0:5]
        for i in range(5):
            self.high_cards[i] = self.high_cards[i] // 4
        #start
        self.judge[9] = self.high_cards[0]*169
        #7.1日添加，在估值函数中考虑高牌大小
        return 9
