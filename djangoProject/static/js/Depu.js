window.alert = function() {
    return false;
}

window.onload = function () {
    var perflop = document.querySelector(".perflop .contents");
    var flop = document.querySelector(".flop .contents");
    var turn = document.querySelector(".turn .contents");
    var river = document.querySelector(".river .contents");
    var compare = document.querySelector(".compare .contents");
    var icons = document.querySelector("#icons");
    var contents = document.querySelector(".contentsDisplay");
    var lis = document.querySelectorAll("ol");
    var jiazhu = document.querySelector(".jiazhu");
    var gongneng = document.querySelector("#gongneng");
    var xiazhu = document.querySelector("#xiazhu");
    var check = document.querySelector(".check");
    var logo = document.querySelector(".logo");
    var cancel = document.querySelector(".cancel");
    // 这里可以稍微修改一下，用H5自定义属性（data-index）加上循环更简洁，只不过我懒得改了（笑cry）
    var round = document.querySelector("#round");
    var ul = round.querySelector("ul");
    var solbut1 = document.querySelector("#solbut1");
    var solbut2 = document.querySelector("#solbut2");
    var solbut3 = document.querySelector("#solbut3");
    var pxa = document.querySelector("#pxa");

    //给三个按钮添加事件
/*    solbut1.onclick = function () {
        ul.style.display = "block";
        pxa.style.display = "none";
    }
    solbut2.onclick = function () {
        ul.style.display = "none";
        pxa.style.display = "block";
    }
    solbut3.onclick = function () {
        ul.style.display = "none";
        pxa.style.display = "none";
    }*/

    //回合的写入函数
    var fun_round = function (dic) {
        var li = document.createElement('li');
        ul.appendChild(li);
        var obj = '自己';
        var mangwei;
        var action;
        if (dic['self'] == "0"){
            obj = '对手';
        }
        if(dic['seat'] == "0"){
            mangwei = "小盲";
        }else{
            mangwei = "大盲";
        }
        switch (dic['action']){
            case "0":
                action = "fold";
                break;
            case "1":
                action = "call";
                break;
            case "2":
                action = "raise";
                break;
            case "3":
                action = "skip";
                break;
            case "4":
                action = "allin";
                break;
            case "5":
                action = "betpot";
                break;
            default:
                console.log("error!");
        }
        li.innerHTML = obj+":"+mangwei+" "+"action"+dic['id']+" "+"行动:"+action+" addmoney:"+dic["add_money"];
    }//fun_round


    lis[0].onclick = function () {
        contents.innerHTML = perflop.innerHTML;
    }
    lis[1].onclick = function () {
        contents.innerHTML = flop.innerHTML;
    }
    lis[2].onclick = function () {
        contents.innerHTML = turn.innerHTML;
    }
    lis[3].onclick = function () {
        contents.innerHTML = river.innerHTML;
    }
    lis[4].onclick = function () {
        contents.innerHTML = compare.innerHTML;
    }
    icons.onclick = function () {
        contents.innerHTML = "<p>Welcome to Depuuuuu</p>";
    }
    var elem = document.querySelector('input[type="range"]');
    //获取一个想显示值的标签，并且初始化默认值
    var target = document.querySelector('.value');
    target.innerHTML = elem.value;

    var rangeValue = function(){
      var newValue = elem.value;
      target.innerHTML = newValue;
    }
    //绑定input监听事件

    elem.addEventListener("input", rangeValue);
    jiazhu.addEventListener("click",function(){
        xiazhu.style.display = "block";
        gongneng.style.display="none";
    })
    check.addEventListener("click", function(){
        xiazhu.style.display = "none";
        gongneng.style.display = "block";
    })
    logo.addEventListener("click",function(){
        window.location.href="/index/";
    })
    cancel.addEventListener("click",function (){
        xiazhu.style.display = "none";
        gongneng.style.display = "block";
    })
}

