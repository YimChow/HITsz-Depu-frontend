from django.db import models


class BaseInfo(models.Model):
    """存储一局的玩家位置、牌等信息"""
    SEAT = (
        (0, 'small_blind'),
        (1, 'big_blind')
    )
    objects = models.Manager()
    my_seat = models.SmallIntegerField(choices=SEAT, default=0)
    my_card1 = models.IntegerField(default=-1)
    my_card2 = models.IntegerField(default=-1)
    opp_card1 = models.IntegerField(default=-1)
    opp_card2 = models.IntegerField(default=-1)
    flop_card1 = models.IntegerField(default=-1)
    flop_card2 = models.IntegerField(default=-1)
    flop_card3 = models.IntegerField(default=-1)

    turn_card = models.IntegerField(default=-1)
    river_card = models.IntegerField(default=-1)
    win_money = models.IntegerField(default=0)


class StatusRecord(models.Model):
    """状态记录，用于在网页读取显示回合记录（说不定还能尝试一下回溯~），写入后不可更改"""
    ROUND = (
        (0, 'pre_flop'),
        (1, 'flop'),
        (2, 'turn'),
        (3, 'river')
    )
    objects = models.Manager()

    # 底池金额
    pots = models.IntegerField(default=150)
    # 更新该条状态信息的action_id
    action_id = models.IntegerField(default=0)
    # 更新该条状态信息的所处阶段
    current_round = models.SmallIntegerField(choices=ROUND, default=0)
    # 更新该条状态信息时的小盲、大盲的已出金（……这个叫啥？？？）
    bb_wager = models.IntegerField(default=100)
    sb_wager = models.IntegerField(default=50)
    # 更新该条状态信息时的小盲、大盲余额
    bb_last = models.IntegerField(default=19900)
    sb_last = models.IntegerField(default=19950)
    # 当前阶段已经raise的次数
    raise_time = models.IntegerField(default=0)
    min_raise_money = models.IntegerField(default=100)


class Action(models.Model):
    """这个是记录一条一条的信息用于显示的"""
    LOCATION = (
        (0, 'small_blind'),
        (1, 'big_blind')
    )
    ACTION_TYPE = (
        (0, 'fold'),
        (1, 'call'),
        (2, 'raise'),
        (3, 'guopai'),
        (4, 'allin'),
        (5, 'betpot'),
    )
    ROUND = (
        (0, 'pre_flop'),
        (1, 'flop'),
        (2, 'turn'),
        (3, 'river')
    )
    objects = models.Manager()
    player = models.SmallIntegerField(choices=LOCATION)
    action = models.SmallIntegerField(choices=ACTION_TYPE)
    current_round = models.SmallIntegerField(choices=ROUND)
    raise_money = models.IntegerField(default=0)
    call_money = models.IntegerField(default=0)
    tips = models.CharField(max_length=20, default="none")





