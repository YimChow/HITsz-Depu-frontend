from django.shortcuts import render
from django.http import JsonResponse
from Poker_algorithm import Function as Fun
import DataManager.StatusRecord as Sr
import DataManager.Action as Ac
from Poker_algorithm.FuncToUse.FuncInstruction import *
from DataManager import Session as Sess
# Create your views here.


def assess(request):
    if request.is_ajax():
        data = request.GET
        return ajax_function(data, request)
    return render(request, "assess.html")


def ajax_function(data, request):
    if data["action"] == "rule":
        if request.user.is_authenticated:
            return JsonResponse({"login": "true"})
        else:
            return JsonResponse({"login": "false"})
    if request.method == 'GET':
        data = request.GET
        if data["action"] == "opp_action":
            action = Fun.OppAI_Action(request, data)
            Sr.AddRecord(request, data)
            records = request.session["StatusRecord"][-1]
            last_action = request.session["Action"][-1]
            baseinfo = request.session['BaseInfo']

            if data["seat"] == 1:# 电脑是大盲
                my_money = records["bb_last"]
            else:
                my_money = records["sb_last"]
            dic = {"pots": records["pots"], "my_money": my_money, "self": data["self"], "seat": data["seat"],
                   "tips": last_action["tips"], "action": str(last_action["action"])}
            response = JsonResponse(dic)
            return response
        if data["action"] == "start_game":
            cards = Fun.GetCards()
            Sess.CreatBaseInfo(request, data, cards)
            Fun.original(data, request)
            response = JsonResponse({"card1": cards[0], "card2": cards[1], "seat": data["seat"]})
            return response

    elif request.method == 'POST':
        data = request.POST
