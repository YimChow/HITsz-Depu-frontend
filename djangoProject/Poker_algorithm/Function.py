import random
from my_web.models import *
from django.forms.models import model_to_dict
from Poker_algorithm.MCTS_frame_new.action_packages import *
import random
import Poker_algorithm.MCTS_frame_new.preflop_data as preflop_data
from Poker_algorithm.packed_combat import Player
from DataManager.Session import *

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


def original(data, request):
    baseinfo = request.session['BaseInfo']
    money = [20000, 20000]
    my_self = Player()
    opp = Player()

    my_self.model.chips = money[0]
    my_self.card = [baseinfo["my_card1"], baseinfo["my_card2"]]
    my_deck = [x for x in range(52)]
    for i in my_self.card:
        my_deck.remove(i)
    my_self.deck = my_deck

    opp_deck = [x for x in range(52)]
    opp.card = [baseinfo["opp_card1"], baseinfo["opp_card2"]]
    opp.model.chips = money[1]
    for i in opp.card:
        opp_deck.remove(i)
    opp.deck = opp_deck

    preflop_table = preflop_data.get_table()
    game = Game()
    game.act_num = 0
    game.bet_amount = 150
    game.set_amount = 10 * (int(sum(money) / 100) / 10)
    if data["seat"] == "1":  # 己方是大盲
        my_self.set = 100
        opp.set = 50
    else:
        my_self.set = 50
        opp.set = 100
    with open('PickleFile/' + baseinfo['pickle_name'], 'wb') as file:
        pickle.dump(game, file)
        pickle.dump(my_self, file)
        pickle.dump(opp, file)
        pickle.dump(preflop_table, file)


def GetCards():
    """
    发牌器
    :return: [a,b,c,d,e,f,g,h,i]共9张，前两张为自己的手牌，然后是对手的手牌，然后是五张公共牌，其中前三张是flop，然后是turn，最后是river
    """
    cards = [i for i in range(51)]
    a = random.sample(cards, 9)
    a = [1,7,51,50,23,32,12,14,9]
    return a


def OppAI_Action(request, data):
    """
    data: 从前端传回的json数据，包括：{action:"opp_action",seat:opp_seat,self:0}(有用的只有seat)
    :return:
    """
    last_status = request.session['StatusRecord'][-1]
    global filename
    global baseinfo
    baseinfo = request.session['BaseInfo']
    filename = 'PickleFIle/'+request.session['BaseInfo']['pickle_name']
    with open(filename, 'rb') as file:
        game = pickle.load(file)
        my_self = pickle.load(file)
        opp = pickle.load(file)
        preflop_table = pickle.load(file)
    try:
        last_action = request.session['Action'][-1]
    except IndexError:
        last_action = {"action": -1, "tips": "none"}
    if last_action["tips"] == "flop_cards":
        current_round = last_status["current_round"] + 1
        RenewModelCards(game, opp, my_self, current_round)
    else:
        current_round = last_status["current_round"]

    if data["seat"] == '0':  # 小盲位
        opp_wager = last_status["bb_wager"]
        my_wager = last_status["sb_wager"]
    else:
        opp_wager = last_status["sb_wager"]
        my_wager = last_status["bb_wager"]

    x = opp.make_action(game, my_self, preflop_table)
    if x == 0:
        new_action = AddOneAction(
            player=data["seat"],
            action=0,
            tips="qipai",
            current_round=current_round,
        )
        request.session['Action'].append(new_action)
        request.session.save()
        SaveModel(game, my_self, opp, preflop_table)
        return 0
    elif x == 1:
        call_money = opp_wager - my_wager
        if call_money == 0:
            action = 3
        else:
            action = 1
        if last_action["tips"] == "flop_cards":
            new_tips = "none"
        else:
            new_tips = "flop_cards"
        new_action = AddOneAction(
            player=data["seat"],
            action=action,
            tips=new_tips,
            call_money=call_money,
            current_round=current_round,
        )

        request.session['Action'].append(new_action)
        request.session.save()
        SaveModel(game, my_self, opp, preflop_table)
        return 1
    elif x == 2:
        add_money = opp.model.bet_amount[-1] * game.set_amount,
        if add_money == my_wager:  # allin
            action = 4
            tips = "to_end"
        else:  # 正常地加注
            action = 2
            tips = "none"
        new_action = AddOneAction(
            player=data["seat"],
            action=action,
            raise_money=int(opp.model.bet_amount[-1] * game.set_amount),
            tips=tips,
            current_round=current_round,
        )
        request.session['Action'].append(new_action)
        request.session.save()
        SaveModel(game, my_self, opp, preflop_table)
        return action


def SaveModel(game, my_self, opp, preflop_table):
    with open(filename, 'wb') as file:
        pickle.dump(game, file)
        pickle.dump(my_self, file)
        pickle.dump(opp, file)
        pickle.dump(preflop_table, file)


def RenewModelCards(game, opp, my_self, current):
    if current == 1:
        new_cards = []
        game.board_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"]]
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
