var flag=-1;/*大盲1，小盲0*/
var opp_seat=-1;/*大盲1，小盲0*/
var my_turn = false;
var end = false;/*标定游戏是否结束*/
var k=0;/*函数五中记录阶段用*/
var cards="";/*前五张为公共牌，最后两张为对手牌，共七张牌*/
/*刚开始的rule和start显示*/
$(document).ready(function(){
    $("#background").css("opacity","0.7");
    $("#rule_board").hide();
    $(".end").hide()
    $(".choice").hide()
    $(".show1").hide();
    /*rule按钮的逻辑代码*/
    $("#rule").click(function(){
    $.ajax({
        url:"/assess",
        data:{"action":"rule"},
        dataType:"json",
        success:function(data){
            if(data["login"]=="true"){
                $(".start_button").hide();
                $("#rule_board").show();
            }
            else{
                alert("请先登录！");
            }
        }
    })
    $("#back").click(function(){
        $("#rule_board").hide();
        $(".start_button").show();
    })
    /*start按钮的逻辑代码*/
    $("#start").click(function(){
        $.ajax({
            url:"/assess",
            data:{"action":"rule"},
            dataType:"json",
            success:function(data){
            if(data["login"]=="true"){
                $(".hide1").hide();
                $(".show1").show();
                $("#background").css("opacity","1");
                ShowSelfCards();
            }
            else{
                alert("请先登录!");
            }
            }
        })
    })

    })
})
/*start后的动画初始化*/

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
                url:"/assess",
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
            wait_opp_action();}
            );
    });
    $(".genpai").click(function(){
        /*给后端传送决策数据*/
        var dtd=$.Deferred();
        var function4=function(dtd){
            $.ajax({
            url:"/assess",
            data:{action:"genpai",seat:flag,self:1},
            dataType:"json",
            success:function(data){
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
            url:"/assess",
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
            url:"/assess",
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
        wait_opp_action();
        });
    });
    $(".qipai").click(function(){
        $(".choice").attr("disabled","true");
        var dtd=$.Deferred();
        var function7 = function(dtd){
            $.ajax({
            url:"/assess",
            data:{action:"qipai",seat:flag},
            datatype:"json",
            success:function(data){
                /*记录行为*/
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
/*打工函数一：翻自己的牌*/
function ShowSelfCards(){
    $(".choice").show();
    $.ajax({
        url:"/assess",
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
/*打工函数三：整理按钮可按与否*/
function SortButton(){
    /*整理按钮的显示，，，因为有点乱就放在单独的函数里了*/
    if(my_turn && end == false){
        $(".choice").attr("disabled",false);
        $.ajax({
            url:"/assess",
            data:{"action":"sort_button"},
            dataType:"json",
            success:function(data){
                if(data["my_wager"]==data["opp_wager"]){
                    $(".genpai").attr("disabled","true")
                }
                /*若己方下注额等于对手，则跟牌按钮失效*/
                if(data["my_wager"]!=data["opp_wager"]){
                    $(".guopai").attr("disabled","true");
                }
                /*若对方最后一次行为是allin，则己方只有qipai和跟牌两个按钮有效*/
                if(data["last_action"] == "4"){
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
        url:"/assess",
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
/*打工函数五：依次翻牌*/
function FlopCards(){
    if(k==0){/*翻三张牌*/
        CardsTypePre(1);
        OppCardsTypePre(1);
        var dtd=$.Deferred();
        var function8 = function(dtd){
            $.ajax({
            url:"/assess",
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

        k=k+1;
    }
    else if(k==2){/*翻最后一张牌*/
        var htm="";
        htm+="<img src=\"../static/image/cards/"+cards[4]+".png\">";
        $("#pub5").html("");
        $("#pub5").append(htm);

    k=k+1;
    }
    else{/*最后比牌阶段，游戏结束*/
        $(".choice").attr("disabled","true");
        $("#loading").hide();
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