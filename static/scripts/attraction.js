let titleFont = document.getElementById("titleLeftFont");
let contentLeft = document.querySelector(".content-left");
let arrowLeft = document.querySelector(".arrow-left");
let arrowRight = document.querySelector(".arrow-right");
let pictureDot = document.querySelector(".dot-btn");
let datetimeInput = document.querySelectorAll(".datetime-input");
let costNum = document.querySelector(".cost-number");
let selectMorning = document.querySelector(".select-time-morning");
let selectAfternoon = document.querySelector(".select-time-afternoon");
let descriptionFont = document.querySelector(".description-font");
let address = document.querySelector(".address-name");
let transport = document.querySelector(".transport");
let url = "/api" + window.location.pathname;
let allRadio, allPc, radio, pcCount;
let pcPosition = 0;

let title = document.querySelector(".title");
let category = document.querySelector(".category");
titleFont.addEventListener("click",function(){
    window.location = "/";
})



//圖片轉播圖
arrowRight.addEventListener("click",function(){
    allPc = document.querySelectorAll(".content-pc");
    allRadio = document.querySelectorAll(".dot");
    if(pcPosition === allPc.length - 1){
        allPc[pcPosition].style.display = "none";
        allPc[0].style.display = "block";
        allRadio[0].checked = true;
        pcPosition = 0;
        return;
    }
    allPc[pcPosition].style.display = "none";
    allPc[pcPosition + 1].style.display = "block";
    allRadio[pcPosition + 1].checked = true;
    pcPosition ++;
});


arrowLeft.addEventListener("click",()=>{
    allPc = document.querySelectorAll(".content-pc");
    allRadio = document.querySelectorAll(".dot");
    if(pcPosition === 0){
        allPc[pcPosition].style.display = "none";
        allPc[allPc.length - 1].style.display = "block";
        allRadio[allPc.length - 1].checked = true;
        pcPosition = allPc.length - 1;
        return;
        
    }
    allPc[pcPosition].style.display = "none";
    allPc[pcPosition - 1].style.display = "block";
    allRadio[pcPosition - 1].checked = true;
    pcPosition --;
})


//點擊下面圓圓切換圖片
function clickDotToChangePc(){
    radio = document.querySelectorAll(".dot");
    for(let i = 0; i < radio.length; i++){//讓每個點點 添加click事件
        radio[i].addEventListener("click",function(){ 
            allRadio = document.querySelectorAll(".dot");
            allPc = document.querySelectorAll(".content-pc");
            for(let k = 0; k < allRadio.length; k++){
                if(allPc[k].style.display === "block"){
                    allPc[k].style.display = "none";
                }
                
                if(allRadio[k].checked === true){
                    if(k != 0){ //一開始載入畫面第0個圖是block，要先把它關掉
                        allPc[0].style.display = "none";
                    }
                    pcPosition = k;
                }
                
            }
            allPc[pcPosition].style.display = "block";
        })
    }
}

//取得圖片並加入點點
fetch(url)
.then((response)=>{
    return response.json()
})
.then((data)=>{
    data = data["data"];
    pcCount = data["images"].length;
    for(let i = 0; i < data["images"].length; i++){
        let newDot = document.createElement("input");
        newDot.type = "radio";
        newDot.name = "control";
        newDot.className = "dot";
        pictureDot.appendChild(newDot);
        let newImg = document.createElement("img");
        newImg.src = data["images"][i];
        newImg.className = "content-pc";
        
        
        if(i > 0){
            newImg.style.display="none";
        }
        contentLeft.insertBefore(newImg,arrowLeft);
        
    }
    document.title = data["name"];
    radio = document.querySelector(".dot");
    radio.checked = true;  //先讓圓圓在第一個
    title.innerHTML = data["name"];
    category.innerHTML = `${data["category"]} at ${data["mrt"]}`;
    descriptionFont.innerHTML = data["description"];
    address.innerHTML = data["address"];
    transport.innerHTML = data["transport"];
    clickDotToChangePc();
})


//顯示費用
selectMorning.addEventListener("click",()=>{
    costNum.innerHTML = "2000元"; 
})

selectAfternoon.addEventListener("click",()=>{
    costNum.innerHTML = "2500元";
})

