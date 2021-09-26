from my_web.models import *


def CreateBaseInfo(data, cards):
    """
    开始游戏时调用一次作为一局的初始信息记录
    :param data: 网页前端传进的json，主要包含位置信息
    :param cards: 九张已抽好的牌
    :return: none
    """
    base_info = BaseInfo(
        my_seat=data["seat"],
        my_card1=cards[0],
        my_card2=cards[1],
        opp_card1=cards[2],
        opp_card2=cards[3],
        flop_card1=cards[4],
        flop_card2=cards[5],
        flop_card3=cards[6],
        turn_card=cards[7],
        river_card=cards[8]
    )

    base_info.save()
