from my_web.models import *
from django.forms.models import model_to_dict
from DataManager.Session import *
try:
    import cPickle as pickle
except:
    import pickle

def AddAction(request, data):
    is_flop = 0
    last_status = request.session['StatusRecord'][-1]

    global baseinfo
    baseinfo = request.session['BaseInfo']
    global filename
    filename = 'PickleFile/' + request.session['BaseInfo']['pickle_name']
    try:
        last_action = request.session['Action'][-1]
    except IndexError:
        last_action = {"tips": "none", "action": -1}
    if last_action["tips"] == "flop_cards":
        current_round = last_status["current_round"] + 1
        # print("current_round" + str(current_round))
        with open(filename, 'rb') as file:
            game = pickle.load(file)
            my_self = pickle.load(file)
            opp = pickle.load(file)
            preflop_table = pickle.load(file)
        RenewModelCards(game, opp, my_self, current_round)
        SaveModel(game, my_self, opp, preflop_table)
    else:
        current_round = last_status["current_round"]
    if data["action"] == "genpai":

        if data["seat"] == '0':  # 小盲位
            opp_wager = last_status["bb_wager"]
            my_wager = last_status["sb_wager"]
        else:
            opp_wager = last_status["sb_wager"]
            my_wager = last_status["bb_wager"]

        call_money = opp_wager - my_wager
        new_action = AddOneAction(
            player=data["seat"],
            action=1,
            current_round=current_round,
            call_money=call_money,
            tips="flop_cards",
        )
        request.session['Action'].append(new_action)
        request.session.save()
        AddModelAction(1, call_money)
        RenewRound(1)# 触发翻牌
        return
    if data["action"] == "jiazhu":
        new_action = AddOneAction(
            player=data["seat"],
            action=2,
            current_round=current_round,
            raise_money=data["wager"],
        )
        request.session['Action'].append(new_action)
        AddModelAction(2, int(data["wager"]))
        RenewRound(0)# 没有触发翻牌
        return
    if data["action"] == "guopai":
        if last_action["tips"] == "flop_cards":
            new_tips = "none"
            RenewRound(0)  # 没有触发翻牌
        else:
            new_tips = "flop_cards"
            RenewRound(1)  # 触发翻牌
        new_action = AddOneAction(
            player=data["seat"],
            action=3,
            current_round=current_round,
            tips=new_tips,
        )
        request.session['Action'].append(new_action)
        AddModelAction(1, 0)
        return
    if data["action"] == "qipai":
        new_action = AddOneAction(
            player=data["seat"],
            action=0,
            current_round=current_round,
        )
        request.session['Action'].append(new_action)
        AddModelAction(0, 0)
        return
    if data["action"] == "allin":
        if data["seat"] == "0":
            add_money = last_status["sb_last"]
        else:
            add_money = last_status["bb_last"]
        new_action = AddOneAction(
            player=data["seat"],
            action=4,
            current_round=current_round,
            call_money=add_money
        )
        request.session['Action'].append(new_action)
        AddModelAction(2, add_money)
        RenewRound(0)  # 没有触发翻牌
        return add_money


def AddModelAction(action, add_money):
    with open(filename, 'rb') as file:
        game = pickle.load(file)
        my_self = pickle.load(file)
        opp = pickle.load(file)
        preflop_table = pickle.load(file)

    my_self.self_action(opp, game, action, add_money)
    with open(filename, 'wb') as file:
        pickle.dump(game, file)
        pickle.dump(my_self, file)
        pickle.dump(opp, file)
        pickle.dump(preflop_table, file)


def RenewModelCards(game, opp, my_self, current):
    if current == 1:
        game.board_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"]]
        new_cards = []
    elif current == 2:
        new_cards = [baseinfo["turn_card"]]
    elif current == 3:
        new_cards = [baseinfo["river_card"]]
        game.board_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                            baseinfo["turn_card"]]
    else:
        new_cards = []
        game.board_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                            baseinfo["turn_card"], baseinfo["river_card"]]
    game.add_card = new_cards
    for i in new_cards:
        opp.deck.remove(i)
        my_self.deck.remove(i)


def SaveModel(game, my_self, opp, preflop_table):
    with open(filename, 'wb') as file:
        pickle.dump(game, file)
        pickle.dump(my_self, file)
        pickle.dump(opp, file)
        pickle.dump(preflop_table, file)


def RenewRound(is_flop):
    with open(filename, 'rb') as file:
        game = pickle.load(file)
        my_self = pickle.load(file)
        opp = pickle.load(file)
        preflop_table = pickle.load(file)

    if is_flop == 0:    # 本action没有触发翻牌，game.counter+=1
        game.counter += 1
    else:
        game.round += 1
        game.counter = 1
    with open(filename, 'wb') as file:
        pickle.dump(game, file)
        pickle.dump(my_self, file)
        pickle.dump(opp, file)
        pickle.dump(preflop_table, file)