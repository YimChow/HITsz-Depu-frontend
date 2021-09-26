import random


def CreatBaseInfo(request, data, cards):
    request.session['BaseInfo'] = {"my_seat": data["seat"], "my_card1": cards[0], "my_card2": cards[1],
                                   "opp_card1": cards[2],
                                   "opp_card2": cards[3], "flop_card1": cards[4], "flop_card2": cards[5],
                                   "flop_card3": cards[6],
                                   "turn_card": cards[7], "river_card": cards[8]}
    request.session['BaseInfo']['pickle_name'] = 'model' + str(random.randint(0, 100)) + '.pkl'

    request.session['StatusRecord'] = []
    request.session['StatusRecord'].append(AddOneStatusRecord(pots=150, action_id=0))
    request.session['Action'] = []
    return


def AddOneStatusRecord(pots=150, action_id=0, current_round=0, bb_wager=100, sb_wager=50, bb_last=19900, sb_last=19950,
                    raise_time=0, min_raise_money=100):
    dic = {"pots": pots, "action_id": action_id, "current_round": current_round, "bb_wager": bb_wager,
           "sb_wager": sb_wager, "bb_last": bb_last, "sb_last": sb_last,
           "raise_time": raise_time, "min_raise_money": min_raise_money, "id": 0}
    return dic


def AddOneAction(player=0, action=0, current_round=0, raise_money=0, call_money=0, tips="none"):
    dic = {"player": player, "action": action, "current_round": current_round, "raise_money": raise_money,
           "call_money": call_money, "tips": tips, "id": 0}
    return dic


