from FuncToUse.FuncInstruction import get_cards_score
from game.enums import ActionType
from game.action import Action
"""
2021.5.27
目前在尝试实现weight-table中遇到的问题：
1.应该重新写一个给牌赋分的方法，其中应该综合考虑：（1）效率问题 （2）牌的潜力问题
2.在牌的得分映射到三种决策行为（以及raise行为的加注）的概率需要考虑。
3.应该还要包括在翻牌前只有两张手牌时对手牌的三种决策行为的赋分

注:可以考虑存储-查找应该会快一些（吧）
"""


class WeightTable(object):
    """采用52阶上三角结构进行存储数据（即WT(i,j)要求i<j)"""
    def __init__(self, host_cards, pub_cards):
        self.host_cards = host_cards
        self.pub_cards = pub_cards
        self.used_cards = host_cards + pub_cards
        self.p_f = [0.33]*1326       # 行主序共（1+51）*51/2个格子（不算对角线）
        self.p_c = [0.34]*1326
        self.p_r = [0.33]*1326         # 初始值，依次代表fold,check/call,bet/raise的概率
        self.pr = [1]*1326           # 初始值每个格子代表的手牌的可能性都为1
        self.no_cards()
        self.init_table()

    def locate(self, i, j):
        """返回52*52（实际上是[0,51]）上格子[i,j]在一维存储空间中对应的下标"""
        if i>j:
            return int((i*(i-1))/2+j)
        elif j>i:
            return int((j*(j-1))/2+i)
        else:
            return -1

    def no_cards(self):
        """将已知牌从WT中剔除"""
        for x in self.used_cards:
            for k in range(0, x):
                self.pr[self.locate(x, k)] = 0
            for k in range(x+1, 52):
                self.pr[self.locate(k, x)] = 0

    def new_pub_cards(self,new_pub_card):
        """新翻出来的公共牌要剔除"""
        self.used_cards = self.used_cards + [new_pub_card]
        for k in range(0,new_pub_card):
            self.pr[self.locate(new_pub_card, k)] = 0
        for k in range(new_pub_card + 1, 52):
            self.pr[self.locate(k, new_pub_card)] = 0

    def wt(self, i, j):
        """返回WT[i][j]的概率"""
        return self.pr[self.locate(i, j)]

    def init_table(self):
        """根据桌面已知牌更新WT中每组手牌的[p_f,p_c,p_r]值"""
        """修改思想是根据每组手牌的牌力进行估计：
            设s为某一组手牌的牌力，最大为300169(肯定不行啊这都超没边儿了，具体怎么给牌力值再看吧）。则：
            p_f = (1-score/300169)*0.3
            p_c = (1-score/300169)*0.7
            p_r = score/300169
            注:以上是我瞎掰的，毫无任何参考价值，实际参数应该经统计或者神经网络估计
        """
        for i in range(1, 52):
            for j in range(i):
                if(self.pr[self.locate(i, j)]!=0):
                    score = get_cards_score([j, i], self.pub_cards)

                    print(i*(i-1)/2+j)  # 测试的时候显示进度

                    index = self.locate(j, i)
                    self.p_f[index] = (1-score/300169)*0.3
                    self.p_c[index] = (1-score/300169)*0.7
                    self.p_r[index] = score/300169

    def up_wt(self, action):
        """根据这个对手的决策行为更新WT表，其中action为Action类的对象"""
        if action.type == ActionType.CALL:
            for x in range(1325):
                self.pr[x] = self.pr[x]*self.p_c[x]
        elif action.type == ActionType.FOLD:
            for x in range(1325):
                self.pr[x] = self.pr[x]*self.p_f[x]
        else:
            for x in range(1325):
                self.pr[x] = self.pr[x]*self.p_r[x]


class Eval(object):
    """注：这个类是模拟对手的类，即host视角给对手建的模型而不是真实的对手模型"""
    def __init__(self, my_cards, pub_cards):
        self.WT = WeightTable(my_cards, pub_cards)

    def do_action(self, action):
        """
        做了什么决策行为后更新wt
        :param action: Action类
        :return: none
        """
        self.WT.up_wt(action)

        for i in range(1,52):   # 测试用，测试的时候要导入action文件用Action类作为参数来进行测试
            for j in range(i):
                print(self.WT.pr[self.WT.locate(i, j)], end='')
            print('\n')
    """
    根据决策更新WT
    """

    """
    根据WT以及上下文进行决策行为，后面在进行simulate时会用到
    """

    """
    看到新pub_cards对WT进行更新
    """