# README----对WeightTable的更新
## 新增内容
1. game包
	- enum.py定义了一些枚举变量
	- action定义决策行为，其中raise会携带筹码信息
2. eval_model包
	- eval_class.py 仅简单编码了WeightTable，没有进行测试，并且里面的参数是随便给的，参考价值不大。
	- 待实现：”对手模型“的各种方法实现以及参数调整，效率分析。
## 未来工作
1. 参考challenge of poker 实现模拟对局版的蒙特卡洛抽样树。
2. 因为有点晚先睡了，总任务规划后说。
	