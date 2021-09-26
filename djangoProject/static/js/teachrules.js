window.onload = function () {
    // var video = document.querySelector("video");
    var icon = document.querySelector(".icon");
    var img1 = document.querySelector(".guize1");
    var img2 = document.querySelector(".guize2");
    var img3 = document.querySelector(".guize3");
    var img4 = document.querySelector(".guize4");
    var img5 = document.querySelector(".guize5");
    var div = document.querySelectorAll(".click");
    var liaotiankuang = document.querySelector(".liaotiankuang");
    var clicktimes = 0;
    div[clicktimes].style.display = "block";
    clickedf = function (e) {
        // content.innerHTML = p[clicktimes].innerHTML;
        if (clicktimes == div.length-1 ) {
            window.location.href="/mainrules/";
        }
        div[clicktimes].style.display = "none";
        clicktimes += 1;
        div[clicktimes].style.display = "block";
        if (clicktimes == 6) {
            img1.style.opacity = "0";
            img1.style.transition = "2s";
            img2.style.opacity = "1";
            img2.style.transition = "2s";
            liaotiankuang.style.top = "430px";
            liaotiankuang.style.transition = "2s";
        }
        else if (clicktimes == 9) {
            img2.style.opacity = "0";
            img2.style.transition = "2s";
            img3.style.opacity = "1";
            img3.style.transition = "2s";
        }
        else if (clicktimes == 11) {
            img3.style.opacity = "0";
            img3.style.transition = "2s";
            img4.style.opacity = "1";
            img4.style.transition = "2s";
        }
        else if (clicktimes == 13) {
            img4.style.opacity = "0";
            img4.style.transition = "2s";
            img5.style.opacity = "1";
            img5.style.transition = "2s";
        }
        else if(clicktimes == div.length - 1){
            img5.style.opacity = "0";
            img5.style.transition = "2s";
            liaotiankuang.style.top = "160px";
            liaotiankuang.style.transition = "2s";
        }
        console.log(clicktimes);
    }
    icon.addEventListener("click", clickedf, false);
}

$(document).ready(function(){
    var css={top:'50px'};
    $(".xiaoren").animate(css,2000,rowBack);
    function rowBack(){
        if(css.top=='50px'){
            css.top='70px';
        }
        else{
            css.top='50px';
        }
        $(".xiaoren").animate(css,2000,rowBack);

    }
})

