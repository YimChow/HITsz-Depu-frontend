var flag=-1;/*大盲1，小盲0*/
var opp_seat=-1;/*大盲1，小盲0*/
var my_turn = false;
var end = false;/*标定游戏是否结束*/
var k=0;/*函数五中记录阶段用*/
var cards="";/*前五张为公共牌，最后两张为对手牌，共七张牌*/
/*开始显示*/
$(document).ready(function(){
    $("#loading").hide()
    $(".end").hide()
    $(".choice").hide()
    $(".show1").hide()
    $(".duigou").hide()
    $("#bb_circle").click(function(){
        flag=1;
        opp_seat=0;
        $("#duigou1").show();
        $("#duigou2").hide();
    })
    $("#sb_circle").click(function(){
        flag=0;
        opp_seat=1;
        $("#duigou2").show();
        $("#duigou1").hide();
    })
    $("#start").click(function(){
        if(flag==-1){
            alert("请先选择盲位！");
        }
        else{
        ShowSelfCards();

        /*翻开自己的牌*/

        CardsTypePre(0)


        /*就两张牌进行预测*/


        /*根据选择决定先行动的人*/
            if(flag==1){
            opp_seat = 0
                /*金额初始化*/
                $("#playermoney2").html("19950");
                $("#playermoney1").html("19900");
                $("#my_pot_num").html("100");
                $("#opp_pot_num").html("50");
                $("#pot_num").html("150");
                /*对手是小盲，询问对手决策*/
                my_turn=false;
                wait_opp_action();
            }
            else{
            opp_seat = 1;
                /*金额初始化*/
                $("#playermoney1").html("19950");
                $("#playermoney2").html("19900");
                $("#my_pot_num").html("50");
                $("#opp_pot_num").html("100");
                $("#pot_num").html("150");
                $("#loading").hide();
                /*己方是小盲。询问己方决策*/
                my_turn=true;
                wait_my_action();
            }
        }

    })
    $("#restart").click(function(){
        $.ajax({
        url:"/mainrules",
        data:{action:"restart"},
        success:function(data){
            
        }
        })
    })
})
/*control的六个按钮*/
$(document).ready(function(){
    /*向后台请求数据并进行处理*/
    /*加注的确认按钮*/
    $(".check").click(function(){
        /*首先要确定加注额是否超过其现有金额*/
        var the_action;
        var subvalue = parseInt(document.querySelector('input[type="range"]').value);
        var wager_last = parseInt($("#playermoney1").html());
        if(subvalue>wager_last){
            alert("加注金额超出现有金额！请重新进行决策！");
        }
        else{
            if(subvalue == wager_last){//实际效果为allin
                the_action = "allin";
            }
            else{
                the_action = "jiazhu";
            }
            var dtd=$.Deferred()
            var function1=function(dtd){
                $.ajax({
                url:"/mainrules",
                data:{action:the_action, wager:subvalue, seat:flag},
                dataType:"json",
                success:function(data){
                    AddMoney(1,data);
                    dtd.resolve();

                }
            })
            return dtd;
            }
        }
        $.when(function1(dtd)).done(function(){
            /*记录行为，然后让对手进行决策*/
            my_turn = false;
            Recorder(1);//self:1 代表自己
            wait_opp_action();}
            );
    });
    $(".genpai").click(function(){
        /*给后端传送决策数据*/
        var dtd=$.Deferred();
        var function4=function(dtd){
            $.ajax({
            url:"/mainrules",
            data:{action:"genpai",seat:flag,self:1},
            dataType:"json",
            success:function(data){
                /*记录己方行为*/

                Recorder(1)/*self:1是己方*/
                AddMoney(1,data);//显示金额更改
                if(data["tips"] == "to_end"){/*说明对方为allin下己方选择跟牌*/
                    while(end == false){
                        FlopCards();
                    }
                }
                else{
                     /*结束己方行为，让对方进行决策*/
                     FlopCards()
                     if(flag == 1){
                        my_turn = true;
                     }
                     else{
                        my_turn = false;
                     }

                }
            dtd.resolve();
            }
        })

        return dtd;
        }
        $.when(function4(dtd)).done(function(){
            wait_opp_action();
        }

        )


    });
    $(".guopai").click(function(){
        var dtd=$.Deferred();
        var function5 = function(dtd){
        $.ajax({
            url:"/mainrules",
            data:{action:"guopai",seat:flag,self:"1"},
            dataType:"json",
            success:function(data){
                Recorder(1);
                if(data["tips"] == "flop_cards"){
                    FlopCards();
                    if(flag == 1){
                    my_turn = true;
                    }
                    else{
                        my_turn = false;
                    }
                }
                else{
                    my_turn = false;
                }
            dtd.resolve();

            }

        })
        return dtd;
        }
        $.when(function5(dtd)).done(
            function(){wait_opp_action();}
        );

    });
    $(".allin").click(function(){
        var dtd=$.Deferred();
        var function6=function(dtd){
        $.ajax({
            url:"/mainrules",
            data:{action:"allin",seat:flag,self:"1"},
            dataType:"json",
            success:function(data){
                AddMoney(1,data);
                dtd.resolve()

            }
        })
        return dtd;
        }
        $.when(function6(dtd)).done(function(){
        /*己方决策完成，让对手进行决策*/
        my_turn = false;
        Recorder(1);
        wait_opp_action();
        });
    });
    $(".qipai").click(function(){
        $(".choice").attr("disabled","true");
        var dtd=$.Deferred();
        var function7 = function(dtd){
            $.ajax({
            url:"/mainrules",
            data:{action:"qipai",seat:flag},
            datatype:"json",
            success:function(data){
                /*记录行为*/
                Recorder(1)/*self:1是己方*/
                while(end == false){
                    FlopCards();
                }
                dtd.resolve()

            }
        })
        return dtd;
        /*游戏结束，没有让对手进行决策的必要*/
        }
        $.when(function7(dtd)).done();

    });
    $(".betpot").click();
})
/*solver界面*/
$(document).ready(function(){
    $("#solver1_all").show();
    $("#solver2_all").hide();
    $("#solver3_all").hide();
    $("#solbut1").click(function(){
        $(".solver_content").show()
        $("#solver1_all").show();
        $("#solver2_all").hide();
        $("#solver3_all").hide();
    })
    $("#solbut2").click(function(){
        $(".solver_content").show()
        $("#solver2_all").show();
        $("#solver1_all").hide();
        $("#solver3_all").hide();
    })
    $("#solbut3").click(function(){
        $(".solver_content").show()
        $("#solver3_all").show();
        $("#solver2_all").hide();
        $("#solver1_all").hide();
    })
})
/*最重要的对手行为、己方行为函数（相互调用）*/
function wait_opp_action(){
    if(end == false){
    if(my_turn==true){
        wait_my_action()
    }
    else{
        var k=$.Deferred();
        var function9 = function(k){
            SortButton();
            /*对手进行决策时的游戏界面显示*/

            setTimeout(function(){k.resolve()},1000);
            return k;
        }
        $.when(function9(k)).done(function(){
            /*向后台请求数据并进行处理*/
            var dtd=$.Deferred();
            var function3 = function(dtd){
            console.log(opp_seat);
            $.ajax({
                url:"/mainrules",
                data:{action:"opp_action",seat:opp_seat,self:0},

                dataType:"json",
                async:true,
                beforeSend:function(){
                    $("#loading").show();
                    $("#userbox1").css("border-color","transparent");
                    $("#userbox2").css("border-color","red");

                },
                success:function(data){
                    /*对手选择弃牌，后端代码自动判输*/
                    if(data["tips"] == "qipai"){
                        while(end == false){
                            FlopCards();
                        }
                    }
                    /*对手选择allin*/
                    else if(data["tips"] == "allin"){
                        AddMoney(0,data);
                        my_turn = true;
                    }
                    /*对手选择过牌并且触发了翻牌条件（包括flop、turn、river和最后的亮牌比较）*/
                    /*显然双方的加注额没有发生变化*/
                    else if(data["tips"] == "flop_cards"){
                        AddMoney(0,data);
                        FlopCards(1,data);
                        if(end == false){//防止翻牌是最后的比较导致游戏结束
                            if(opp_seat == 1){/*对手是大盲位*/
                                my_turn = false;
                            }
                            else{
                                my_turn = true;
                            }
                        }
                    }
                    /*to_end为己方的上一个行为为all_in带来的当前的这个决策具有决定性影响*/
                    /*若为弃牌已经被上面的“qipai”捕获，因此此处为选择check的决策*/
                    else if(data["tips"] == "to_end"){
                        AddMoney(0,data);
                        while(end == false){
                            FlopCards();
                        }
                    }

                    /*就是除了以上情况外，只有金额变化的决策：加注、过牌*/
                    else{
                    console.log(data)
                        AddMoney(0,data);
                        my_turn = true;
                    }
                dtd.resolve()

                }
            })
            return dtd;
            }
            $.when(function3(dtd)).done(
            function(){
            /*记录、更新牌型概率、让对方进行决策*/
            Recorder(0);
            wait_my_action();}
        )
        });
    }
    }

}
function wait_my_action(){
    if(end == false){
    if(my_turn==false){
    wait_opp_action();
    }
    else{
        $("#loading").hide();
        /*看按钮哪些能按,赋权*/
        SortButton();
        /*己方进行决策时的游戏界面显示*/
        $("#userbox2").css("border-color","transparent");
        $("#userbox1").css("border-color","red");
    }
    }
}


/*打工函数一：翻自己的牌*/
function ShowSelfCards(){
    $(".choice").show();
    $.ajax({
        url:"/mainrules",
        data:{"action":"start_game","round":0,"seat":flag},
        dataType:"json",
        success:function(data){
            $("#gameback").css("opacity","1.0");
            $("#gameback").attr("src","../static/image/gameback.png");
            $(".hide1").hide()
            $(".show1").fadeIn(3000)
            $("#loading").hide();
            var htm = "";
            htm+="<img src=\"../static/image/cards/"+data["card1"]+".png\">";
            $("#mycard1").html("");
            $("#mycard1").append(htm);
            htm="";
            htm+="<img src=\"../static/image/cards/"+data["card2"]+".png\">";
            $("#mycard2").html("");
            $("#mycard2").append(htm);
            CardsTypePre("0");

        }
    })
}
/*打工函数二：显示己方牌的概率和敌方牌的概率*/
function CardsTypePre(round){
    $.ajax({
        url:"/mainrules",
        data:{"action":"CardsType","round":round},
        dataType:"json",
        success:function(data){
            $("#curr_type").html(data["current_type"]);
            $("#type1").html(data["0"]);
            $("#type2").html(data["1"]);
            $("#type3").html(data["2"]);
            $("#type4").html(data["3"]);
            $("#type5").html(data["4"]);
            $("#type6").html(data["5"]);
            $("#type7").html(data["6"]);
            $("#type8").html(data["7"]);
            $("#type9").html(data["8"]);
            $("#type10").html(data["9"]);

        }
    })
}
function OppCardsTypePre(round){
    $.ajax({
        url:"/mainrules",
        data:{"action":"OppCardsType","round":round},
        dataType:"json",
        success:function(data){
            $("#opp_curr_type").html(data["current_type"]);
            $("#opp_type1").html(data["0"]);
            $("#opp_type2").html(data["1"]);
            $("#opp_type3").html(data["2"]);
            $("#opp_type4").html(data["3"]);
            $("#opp_type5").html(data["4"]);
            $("#opp_type6").html(data["5"]);
            $("#opp_type7").html(data["6"]);
            $("#opp_type8").html(data["7"]);
            $("#opp_type9").html(data["8"]);
            $("#opp_type10").html(data["9"]);

        }

    })
}
/*打工函数三：整理按钮可按与否*/
function SortButton(){
    /*整理按钮的显示，，，因为有点乱就放在单独的函数里了*/
    if(my_turn && end == false){
        $(".choice").attr("disabled",false);
        $.ajax({
            url:"/mainrules",
            data:{"action":"sort_button"},
            dataType:"json",
            success:function(data){
                console.log(data["last_action"])
                /*若己方下注额小于对手，则过牌按钮失效*/
                console.log(data["my_wager"])
                console.log(data["opp_wager"])
                if(data["my_wager"]==data["opp_wager"]){
                    $(".genpai").attr("disabled","true")
                }
                /*若己方下注额等于对手，则跟牌按钮失效*/
                if(data["my_wager"]!=data["opp_wager"]){
                    $(".guopai").attr("disabled","true");
                }
                /*若对方最后一次行为是allin，则己方只有qipai和跟牌两个按钮有效*/
                if(data["last_action"] == "4"){
                    console.log(data["last_action"]);
                    $(".jiazhu").attr("disabled","true");
                    $(".betbot").attr("disabled","true");
                    $(".allin").attr("disabled","true");
                }

            }
        })
    }
    else{
        $(".choice").attr("disabled","true");
    }
}
/*打工函数四：最后作比较*/
function Compare(){
    /*最后的比牌*/
    $.ajax({
        url:"/mainrules",
        data:{"action":"compare",seat:"flag"},
        dataType:"json",
        success:function(data){
            $("#gameback").hide()
            $(".show1").hide()
            var win_money = 0;
            if(data["is_win"] == "0"){
                $("#win_bg").fadeIn(1000);
                $("#lost_bg").removeClass("end");
                $("#draw_bg").removeClass("end");
                win_money = parseInt($("#pot_num").html())-parseInt($("#my_pot_num").html())
            }
            else if(data["is_win"] == "2"){
                $("#lost_bg").fadeIn(1000);
                $("#win_bg").removeClass("end");
                $("#draw_bg").removeClass("end");
                win_money = "-"+$("#my_pot_num").html()

            }
            else{
                $("#draw_bg").fadeIn(1000);
                $("#win_bg").removeClass("end");
                $("#lost_bg").removeClass("end");
            }

            $("#opp_card1").attr('style',"top:130px;left:-269px");
            $("#opp_card2").attr('style',"top:130px;left:-199px");
            $("#mycard1").attr('style',"top:230px;left:100px");
            $("#mycard2").attr('style',"top:230px;left:170px");
            $("#pubcards").attr('style',"top:330px;left:100px");
            var opp_type=$("#opp_curr_type").html();
            var my_type=$("#curr_type").html();
            $("#end_text4").html(opp_type)
            $("#end_text5").html(my_type)
            $("#end_text6").html("赢金："+win_money)
            $(".end").fadeIn(3000);
            /*$(".end").addClass('magictime vanishIn')*/
        }
    })
}
/*打工函数五：记录新Action*/
function Recorder(self) {
/*self:0是对手，1是己方*/
    var dic;
    $.ajax({
        url:"/mainrules",
        data:{"action":"records","self":self},
        dataType:"json",
        success:function(data){
            dic=data;
            console.log(dic);
            var round = document.querySelector("#round");
    var table = round.querySelector("table");
    var tr = document.createElement('tr');
    table.appendChild(tr);
    var obj = '自己';
    var mangwei;
    var action;
    if (dic["self"] == "0"){
        obj = '对手';
        tr.classList.add("opp_record")
    }
    else{
        tr.classList.add("self_record")
    }

    if(dic['seat'] == "0"){
        mangwei = "小盲";
    }else{
        mangwei = "大盲";
    }
    switch (dic['action']){
        case 0:
            action = "fold";
            break;
        case 1:
            action = "call";
            break;
        case 2:
            action = "raise";
            break;
        case 3:
            action = "skip";
            break;
        case 4:
            action = "allin";
            break;
        case 5:
            action = "betpot";
            break;
        default:
            console.log("error!");
    }
    var htm;
    console.log(dic['action'])
    htm = "<td>"+dic['id']+"</td><td>"+mangwei+"</td><td>"+action+"</td><td>"+dic["add_money"]+"</td>"
    tr.innerHTML = htm
        }
    })

}//fun_round
/*打工函数五：依次翻牌*/
function FlopCards(){
    if(k==0){/*翻三张牌*/
        CardsTypePre(1);
        OppCardsTypePre(1);
        var dtd=$.Deferred();
        var function8 = function(dtd){
            $.ajax({
            url:"/mainrules",
            data:{"action":"flop_cards"},
            dataType:"json",
            success:function(data){
                cards=data["cards"].split(",");
                var htm = "";
                htm+="<img src=\"../static/image/cards/"+cards[0]+".png\">";
                $("#pub1").html("");
                $("#pub1").append(htm);
                htm = ""
                htm+="<img src=\"../static/image/cards/"+cards[1]+".png\">";
                $("#pub2").html("");
                $("#pub2").append(htm);
                htm = ""
                htm+="<img src=\"../static/image/cards/"+cards[2]+".png\">";
                $("#pub3").html("");
                $("#pub3").append(htm);
                CardsTypePre(1);
                OppCardsTypePre(1);
                dtd.resolve()
            }
        })

        return dtd;
        }
        $.when(function8(dtd)).done(function(){
             k=k+1;}
        )


    }
    else if(k==1){/*翻一张牌*/
        var htm="";
        htm+="<img src=\"../static/image/cards/"+cards[3]+".png\">";
        $("#pub4").html("");
        $("#pub4").append(htm);
        CardsTypePre(2)
        OppCardsTypePre(2)

        k=k+1;
    }
    else if(k==2){/*翻最后一张牌*/
        var htm="";
        htm+="<img src=\"../static/image/cards/"+cards[4]+".png\">";
        $("#pub5").html("");
        $("#pub5").append(htm);
        CardsTypePre(3)
        OppCardsTypePre(3)

    k=k+1;
    }
    else{/*最后比牌阶段，游戏结束*/
        $(".choice").attr("disabled","true");
        $("#loading").hide();
        CardsTypePre(3);
        OppCardsTypePre(4);
        var htm = ""
        $("#opp_back").hide()
        htm+="<img src=\"../static/image/cards/"+cards[5]+".png\">";
        $("#opp_card1").html("");
        $("#opp_card1").append(htm);
        htm = "";
        htm+="<img src=\"../static/image/cards/"+cards[6]+".png\">";
        $("#opp_card2").html("");
        $("#opp_card2").append(htm);
        $("#userbox1").css("border-color","transparent");
        $("#userbox2").css("border-color","transparent");
        my_turn = false;
        end = true;
        setTimeout(function(){
            Compare();
        },5000);

    }
}
/*打工函数六：显示金额更改*/
function AddMoney(self,data){
    if(self == 0){
        var target = document.querySelector('#playermoney2');
        $("#opp_pot_num").html(20000-parseInt(data["my_money"]))
    }
    else{
        var target = document.querySelector('#playermoney1');
        $("#my_pot_num").html(20000-parseInt(data["my_money"]))
    }
    target.innerHTML = data["my_money"];
    target = document.querySelector('#pot_num');
    target.innerHTML = data["pots"];
}