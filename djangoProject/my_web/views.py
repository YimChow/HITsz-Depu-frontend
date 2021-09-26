from django.shortcuts import render
from django.http import JsonResponse
from Poker_algorithm import Function as Fun
import DataManager.BaseInfo as Bi
import DataManager.StatusRecord as Sr
import DataManager.Action as Ac
from my_web.models import *
from django.forms.models import model_to_dict
from Poker_algorithm.FuncToUse.FuncInstruction import *
from DataManager import Session as Sess


# Create your views here.


def index(request):
    #  HttpResponse("hello world!")
    return render(request, "index.html")


def introduction(request):
    return render(request, "introduction.html")


def mainrules(request):
    if request.is_ajax():
        if request.method == 'GET':
            data = request.GET

            if data["action"] == "restart":
                request.session["BaseInfo"] = {}
                request.session["Action"] = []
                request.session["StatusRecord"] = []
                return JsonResponse({})
            if data["action"] == "opp_action":
                # 对于对手的action，最初传入data和进行决策的相关信息。在该函数内部完成：进行决策、将决策信息录入action数据库中
                action = Fun.OppAI_Action(request, data)
                Sr.AddRecord(request, data)
                records = request.session['StatusRecord'][-1]
                last_action = request.session['Action'][-1]
                last_status = records
                baseinfo = request.session['BaseInfo']

                if data["seat"] == "1":
                    my_money = records["bb_last"]
                else:
                    my_money = records["sb_last"]
                print("opp_seat"+str(data["seat"]))
                dic = {"pots": records["pots"], "my_money": my_money, "self": data["self"], "seat": data["seat"],
                       "tips": last_action["tips"], "action": str(last_action["action"])}
                response = JsonResponse(dic)
                return response

            """以下是改版用的一些函数"""
            # 已session化
            if data["action"] == "start_game":
                # _round = request.GET.get("round")
                # 起牌
                cards = Fun.GetCards()
                # 创建这一局的记录于session["BaseInfo"]中,并初始化StatusRecords、Action
                Sess.CreatBaseInfo(request, data, cards)
                # 初始化当前牌局信息和action数据表以及唤醒后端德扑AI
                Fun.original(data, request)
                # 回应前端
                response = JsonResponse({"card1": cards[0], "card2": cards[1], "seat": data["seat"]})
                return response
            # 已session化
            if data["action"] == "flop_cards":
                baseinfo = request.session['BaseInfo']
                cards = str(baseinfo["flop_card1"]) + ',' + str(baseinfo["flop_card2"]) + ',' + str(
                    baseinfo["flop_card3"]) + ',' + str(baseinfo["turn_card"]) + ',' + str(baseinfo["river_card"]) \
                        + ',' + str(baseinfo["opp_card1"]) + ',' + str(baseinfo["opp_card2"])
                return JsonResponse({"cards": cards})
            # 已session化
            if data["action"] == "records":
                last_action = request.session['Action'][-1]
                last_record = request.session['StatusRecord'][-1]
                baseinfo = request.session['BaseInfo']
                dic = {"action": last_action["action"], "id": len(request.session['Action']),
                       "add_money": int(last_action["raise_money"]) + int(last_action["call_money"]), "self": data["self"]}
                if data["self"] == "1":
                    dic["seat"] = baseinfo["my_seat"]
                elif baseinfo["my_seat"] == "1":
                    dic["seat"] = "0"
                else:
                    dic["seat"] = "1"
                return JsonResponse(dic)
            # 已sessio化
            if data["action"] == "compare":
                baseinfo = request.session['BaseInfo']
                last_action = request.session['Action'][-1]
                if last_action["action"] == "0":
                    if last_action["player"] == baseinfo["my_seat"]:
                        status = 2
                    else:
                        status = 0
                else:
                    status = is_win([baseinfo["my_card1"], baseinfo["my_card2"]],
                                    [baseinfo["opp_card1"], baseinfo["opp_card2"]],
                                    [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                                     baseinfo["turn_card"], baseinfo["river_card"]])

                return JsonResponse({"is_win": status})
            # 已session化
            if data["action"] == "qipai":
                Ac.AddAction(request, data)
                Sr.AddRecord(request, data)
                return JsonResponse({"tips": "qipai"})
            # 已session化
            if data["action"] == "genpai":
                try:
                    last_action = request.session['Action'][-1]
                    if last_action["action"] == "4":
                        tips = "to_end"
                    else:
                        tips = "none"
                except:
                    tips = "none"
                Ac.AddAction(request, data)
                Sr.AddRecord(request, data)
                records = request.session['StatusRecord'][-1]
                last_action = request.session['Action'][-1]

                dic = {"pots": records["pots"], "my_money": records["sb_last"], "seat": data["seat"],
                       "action": str(last_action["action"]),
                       "add_money": int(last_action["raise_money"]) + int(last_action["call_money"]),
                       "self": data["self"], "tips": tips}

                if data["seat"] == "0":
                    dic["my_money"] = records["sb_last"]
                else:
                    dic["my_money"] = records["bb_last"]

                response = JsonResponse(dic)
                return response
            # 已session化
            if data["action"] == "sort_button":
                records = records = request.session['StatusRecord'][-1]
                try:
                    action = request.session['Action'][-1]
                except:
                    action = {"action": -1}
                response = JsonResponse(
                    {"my_wager": records["bb_last"], "opp_wager": records["sb_last"],
                     "last_action": str(action["action"]),
                     "curr_round": records["current_round"]})
                return response
            # 已session化
            if data["action"] == "CardsType":
                baseinfo = request.session['BaseInfo']
                known_cards = [baseinfo["my_card1"], baseinfo["my_card2"]]
                if data["round"] == "1":
                    known_cards += [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"]]
                elif data["round"] == "2":
                    known_cards += [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                                    baseinfo["turn_card"]]
                elif data["round"] == "3":
                    known_cards += [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                                    baseinfo["turn_card"], baseinfo["river_card"]]
                response = type_forcaster(known_cards)
                response["current_type"] = " "
                if data["round"] != "0":
                    response["current_type"] = get_type(known_cards)
                return JsonResponse(response)
            # 已session化
            if data["action"] == "OppCardsType":
                baseinfo = request.session['BaseInfo']
                self_cards = [baseinfo["my_card1"], baseinfo["my_card2"]]
                pub_cards = []
                if data["round"] == "1":
                    pub_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"]]
                elif data["round"] == "2":
                    pub_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                                 baseinfo["turn_card"]]
                elif data["round"] == "3":
                    pub_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                                 baseinfo["turn_card"], baseinfo["river_card"]]

                response = opp_type_forcaster(self_cards, pub_cards)
                response["current_type"] = "待定"

                if data["round"] == "4":
                    pub_cards = [baseinfo["flop_card1"], baseinfo["flop_card2"], baseinfo["flop_card3"],
                                 baseinfo["turn_card"], baseinfo["river_card"]]
                    opp_cards = [baseinfo["opp_card1"], baseinfo["opp_card2"]]
                    response = type_forcaster(opp_cards + pub_cards)
                    response["current_type"] = get_type(opp_cards + pub_cards)
                return JsonResponse(response)
            # 已session化
            if data["action"] == "allin":
                add_money = Ac.AddAction(request, data)
                Sr.AddRecord(request, data)
                record = request.session['StatusRecord'][-1]

                baseinfo = request.session['BaseInfo']
                dic = {"my_money": 0, "seat": data["seat"], "pots": record["pots"], "self": data["self"],
                       "action": "4", "tips": "none",
                       "add_money": add_money}
                return JsonResponse(dic)
            # 已session化
            if data["action"] == "jiazhu":
                Ac.AddAction(request, data)
                Sr.AddRecord(request, data)
                records = request.session['StatusRecord'][-1]
                last_action = request.session['Action'][-1]

                dic = {"pots": records["pots"], "my_money": records["sb_last"], "seat": data["seat"],
                       "action": str(last_action["action"]),
                       "add_money": int(last_action["raise_money"]) + int(last_action["call_money"]),
                       "id": len(request.session['Action']),
                       "self": "1"}

                if data["seat"] == "0":

                    dic["my_money"] = records["sb_last"]
                else:
                    dic["my_money"] = records["bb_last"]

                response = JsonResponse(dic)
                return response
            # ok
            if data["action"] == "guopai":
                Ac.AddAction(request, data)
                Sr.AddRecord(request, data)
                last_action = request.session['Action'][-1]
                dic = {"tips": last_action["tips"]}
                response = JsonResponse(dic)
                return response

        if request.method == 'POST':
            pass

    return render(request, "mainrules.html")


def teachrules(request):
    return render(request, "teachrules.html")


def login(request):
    return render(request, "user.html")
