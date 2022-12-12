let title = document.querySelector(".booking-title");
let bookingEmpty = document.querySelector(".booking-empty");
let bookingContent = document.querySelector(".booking-content");
let totalCost = document.querySelector(".total-price");
let hr = document.querySelectorAll(".hr");
let contactInformation = document.querySelector(".contact-information");
let creditCardInformation = document.querySelector(".credit-card-information");
let priceAndBtn = document.querySelector(".price-and-btn");
let emptyShoppingcart = document.querySelector(".empty-shoppingcart");
let bookingMessage = document.querySelector(".booking-message");
let darker = document.querySelector(".darker");
let bookingMessageClose = document.querySelector(".booking-message-btn");
let bookingMessageFont = document.querySelector(".booking-message-font");

let userName, data, time, productImage, productTitle, productDate, productTime, productPrice, productAddress, trashcan;
let newDiv, newImg, newP, attractionId, productName;
let count = 0;
let totalPrice = 0;
fetch("/api/user/auth")
.then((response)=>{
    return response.json()
})
.then((data)=>{
    userName = data['data']['name'];
    title.innerHTML = `您好，${userName}，待預訂的行程如下 :`;
})

fetch("/api/booking")
.then((response)=>{
    return response.json()
})
.then((data)=>{
    if("data" in data){
        if(data.data.length === 0){
            bookingEmpty.style.display = "block";
            hr[0].style.display = "none";
            hr[1].style.display = "none";
            hr[2].style.display = "none";
            contactInformation.style.display = "none";
            creditCardInformation.style.display = "none";
            priceAndBtn.style.display = "none";
            emptyShoppingcart.style.display = "block";
        }else{
            data = data.data;
            for(let i = 0; i < data.length; i++){
                produceProductHTML();
                productImage = document.querySelectorAll(".product-image");
                productTitle = document.querySelectorAll(".right-product-title");
                productDate = document.querySelectorAll(".product-date");
                productTime = document.querySelectorAll(".product-time");
                productPrice = document.querySelectorAll(".product-price");
                productAddress = document.querySelectorAll(".product-address");
                productImage[i].src = data[i].attraction.image;
                productTitle[i].innerHTML =`台北一日遊 : ${data[i].attraction.name}`;
                productDate[i].innerHTML = `日期 : ${data[i].date}`;
                if(data[i].time === "morning"){
                    time = "早上9點到下午4點";
                    totalPrice += 2000;
                }else{
                    time = "下午5點到晚上8點";
                    totalPrice += 2500;
                }
                productTime[i].innerHTML = `時間 : ${time}`;
                productPrice[i].innerHTML =`費用 :  ${data[i].price}`;
                productAddress[i].innerHTML =`地點 :  ${data[i].attraction.address}`;
                trashcan = document.querySelectorAll(".trashcan");
                trashcan[i].addEventListener("click",()=>{ //刪除booking資料
                    productName = data[i].attraction.name
                    fetch(`/api/attractions?keyword=${productName}`)
                    .then((response)=>{
                        return response.json()
                    })
                    .then((data)=>{
                        attractionId = data.data[0].id;
                    })
                    .then(()=>{
                        fetch("/api/booking",{
                            method : 'DELETE',
                            body:JSON.stringify({
                                "attractionId" : `${attractionId}`
                            }),
                            headers:{
                                'Content-type':'application/json; charset=UTF-8',
                            },
                        })
                        .then((response)=>{
                            return response.json()
                        })
                        .then((data)=>{
                            if("ok" in data){
                                
                                bookingMessage.style.display = "block";
                                darker.style.display = "block";
                            }
                            if("error" in data){
                                bookingMessage.style.display = "block";
                                darker.style.display = "block";
                                bookingMessageFont.innerHTML = "刪除失敗";
                            }
                        })
                        
                    })    
                })
                
            }
            totalCost.innerHTML = `總價 : 新台幣${totalPrice}元`;
            
        }
    }
})


bookingMessageClose.addEventListener("click",()=>{
    bookingMessage.style.display = "none";
    darker.style.display = "none";
    location.reload();
})


//產生產品的HTML
function produceProductHTML(){
    newDiv = document.createElement("div");
    newDiv.className = "booking-product";
    bookingContent.appendChild(newDiv);
    let bookingProduct = document.querySelectorAll(".booking-product");
    newDiv = document.createElement("div");
    newDiv.className = "left-product";
    bookingProduct[count].appendChild(newDiv);
    newImg = document.createElement("img");
    newImg.className = "product-image";
    let leftProduct = document.querySelectorAll(".left-product");
    leftProduct[count].appendChild(newImg);
    newDiv = document.createElement("div");
    newDiv.className = "right-product";
    bookingProduct[count].appendChild(newDiv);
    newDiv = document.createElement("div");
    newDiv.className = "right-product-img-title";
    let rightProduct = document.querySelectorAll(".right-product");
    rightProduct[count].appendChild(newDiv);
    let rightProductImgTitle = document.querySelectorAll(".right-product-img-title")
    newP = document.createElement("p");
    newP.className = "right-product-title";
    rightProductImgTitle[count].appendChild(newP);
    newImg = document.createElement("img");
    newImg.className = "trashcan";
    newImg.src = "../static/images/icon_delete.png"
    rightProductImgTitle[count].appendChild(newImg);
    newP = document.createElement("p");
    newP.className = "product-date";
    rightProduct[count].appendChild(newP);
    newP = document.createElement("p");
    newP.className = "product-time";
    rightProduct[count].appendChild(newP);
    newP = document.createElement("p");
    newP.className = "product-price";
    rightProduct[count].appendChild(newP);
    newP = document.createElement("p");
    newP.className = "product-address";
    rightProduct[count].appendChild(newP);
    
    count ++;
}