from my_web.models import *
from django.forms.models import model_to_dict
from DataManager.Session import *


def AddRecord(request, data):
    last_record = request.session['StatusRecord'][-1]
    new_action = request.session['Action'][-1]

    add_money = int(new_action["raise_money"]) + int(new_action["call_money"])
    new_pots = last_record["pots"] + add_money
    current_round = new_action["current_round"]
    action_id = new_action["id"]
    bb_wager = last_record["bb_wager"]
    sb_wager = last_record["sb_wager"]
    bb_last = last_record["bb_last"]
    sb_last = last_record["sb_last"]

    if data["seat"] == '0':   # 小盲
        sb_wager = last_record["sb_wager"] + add_money
        sb_last = last_record["sb_last"] - add_money
        print(sb_last)
    else:
        bb_wager = last_record["bb_wager"] + add_money
        bb_last = last_record["bb_last"] - add_money

    new_status = AddOneStatusRecord(
        pots=new_pots,
        action_id=action_id,
        bb_wager=bb_wager,
        sb_wager=sb_wager,
        bb_last=bb_last,
        sb_last=sb_last,
        current_round=current_round,
    )
    request.session['StatusRecord'].append(new_status)
    request.session.save()
