window.onload = function (){
    var box1 = document.querySelector(".box1");
    var box2 = document.querySelector(".box2");
    box1.addEventListener("mouseover",function(){
        box1.style.transform = "rotateY(180deg)";
    })
    box2.addEventListener("mouseover",function(){
        box2.style.transform = "rotateY(180deg)";
    })
}
$(document).ready(function(){
    $("#start_choice").slideUp()
    $("#to_table").click(function(){
        $("#start_choice").slideDown()
        var target=$("#table").offset().top;
        $("html,body").animate({scrollTop:target}, 1500);
    })
})