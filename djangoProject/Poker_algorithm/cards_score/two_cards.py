"""
这个文件尝试生成并存储对两张手牌的牌里的评估
思路:
1.先生成当前手牌的未来各种牌型出现的概率(已经完成辣！可以看到高牌、对子的概率都大差不差的)
2.对这些概率&&牌面大小&&花色异同进行映射赋分
"""
from FuncToUse.FuncInstruction import get_type
from random import sample

file_name = 'two_cards.txt'
with open(file_name,'a+') as f:
    try:
        for i in range(48,52):
            for j in range(i):
                types=[0]*10
                test_time=30000
                cards = [x for x in range(52)]
                cards.remove(i)
                cards.remove(j)

                for k in range(test_time):
                    other_cards = sample(cards,5)
                    type = get_type([i,j]+other_cards)
                    types[type]+=1

                f.write(str(i)+'\t'+str(j)+'\t')
                for _ in range(10):
                    f.write(str(types[_]/test_time)+'\t')
                f.write('\n')
    except:
        pass
