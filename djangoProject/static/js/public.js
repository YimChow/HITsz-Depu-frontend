$(document).ready(function(){
    $("#down").hide()
    $("#up").click(function(){
        $("#navcontainer").slideToggle();
        setTimeout(function(){
        $("#down").show();
        },500)

    })
    $("#down").click(function(){
        $("#navcontainer").slideToggle();
        $("#down").hide();
    })

    $(".nav_menu1").hover(
        function(){
            $(this).find("div").removeClass("list2");
            $(this).find("div").addClass("list1");
        },
        function(){
            $(this).find("div").removeClass("list1");
            $(this).find("div").addClass("list2");
        }
    )
})