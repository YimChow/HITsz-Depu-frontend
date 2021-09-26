import random

class Opponent_Model(object):
    # 对手模型，内容会随项目推进继续补充
    def __init__(self):
        self.possible_set = []
        self.action_set = []
        self.action_status = 1
        # 理解为一个函数的返回值，即self.is_agressive ((((可以定义在类里但我忘了
        self.bet_amount = [] #默认1底池
        self.distribution = [0, 0, 0]
        self.round = 0
        self.chips = 0
        # action_status: 7.15日引入
        # 分暂时为 1和2：
        # 1是保守决策状态，2是激进决策状态
        # distribution 存储对象的对手此次操作的分布列表
        # round: 7.26日引入，记录此时处于第几轮，用于有加注的决策判断

'''
7.29代码结构优化想法，将己方视角牌库和手牌当做对象的属性来处理
要改挺多的，暂时没改动
'''

def calculate_raise_amount(distribution):
    action = 0
    if distribution[0] > distribution[2]:
        i = random.randint(1,2)
        if i == 1:
            action = 0.5
        else:
            action = 1
    else:
        new_set = [distribution[0],distribution[0]+distribution[1],sum(distribution)]
        x = random.randint(1, sum(distribution))
        reflection = sum(distribution)
        raise_set = [0.5, 1, 2]
        # 可以设置的更加多样，并且也可以设置为范围内连续，但为了方便测试先设置成半底池，1倍和2倍三种情况
        for i in range(3):
            if new_set[i] == 0: continue
            if abs(1-x/new_set[i]) < reflection:
                reflection = abs(1-(x/new_set[i]))
                action = raise_set[i]
    # print("raise time: "+str(action))
    return action


def status_evaluation(our_model, opp_model):
    # 根据our_model和opp_model综合评估出当前our_model的决策状态
    # 7.25：判断函数判断标准将不再利用最近的行为的标准，而是评估后的决策状态
    # 评估结果具有小范围的随机性（主要在边缘牌值的计算上
    # 暂时的思路边缘状态中将==1和==2结合使用
    if abs(len(our_model.action_set)-len(opp_model.action_set)) > 1\
            or len(our_model.action_set) < len(opp_model.action_set):
        # 因为是行动完后进行的状态评估，所以己方行为次数至少不小于对方次数
        # 以防出错
        print("action set length not suited, ERROR!")
        return
    if len(our_model.action_set) == 0:
        print("ERROR in Evaluation")
        return
    '''
    关于为什么要判断先后手：相对后手，行为对应的状态会偏向激进
    而先手则基本上与行为决策所挂钩，但如果进入持续加注阶段，这种差异将会消去
    '''
    if len(our_model.action_set) == 1:
        if len(opp_model.action_set) == 0:
            our_model.action_status = our_model.action_set[-1]
        elif len(opp_model.action_set) == 1:
            if opp_model.action_set[-1] == 1:
                if our_model.action_set[-1] == 1:
                    our_model.action_status = 1
                elif our_model.action_set[-1] == 2:
                    if our_model.bet_amount == 0.5 \
                            and len(opp_model.action_set) > len(opp_model.bet_amount) + opp_model.round:
                        x = random.randint(1,2)
                        our_model.action_status = x
                        # 0.5底池我们认为是边界

def next_phace(model_set):
    for model in model_set:
        model.round += 1
    return

def cards_visualize(cards):
    suit = ["♥","♦","♣","♠"]
    face = ['2 ','3 ', '4 ', '5 ','6 ','7 ','8 ','9 ','10 '
            ,'J ','Q ','K ','A ']
    a = ""
    for card in cards:
        #print(str(suit[int(card%4)]+face[int(card/4)]),end="")
        a += str(suit[int(card%4)]+face[int(card/4)])
    #print("")
    return a



if __name__ =="__main__":
    '''calculate_raise_amount([1356,7845,9847])
    a = Opponent_Model()
    b = Opponent_Model()
    status_evaluation(a,b)'''
    cards_visualize([13,15,50])