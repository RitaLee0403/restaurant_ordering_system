let content = document.querySelector(".content");
let historyOrderEmptyImg = document.querySelector(".order_history_empty");
let newDiv, newImg, newP;
let count;



getHistoryOrder();












function getHistoryOrder(){
    count = 0;
    fetch("/api/history_order")
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        if(data.length === 0){
            historyOrderEmptyImg.style.display = "block";
            return;
        }
        for(let i = 0; i < data.length; i++){
            newDiv = document.createElement("div");
            newDiv.className = "order-content";
            content.appendChild(newDiv);

            let orderContent = document.querySelectorAll(".order-content");
            newDiv = document.createElement("div");
            newDiv.className = "order-content-left";
            orderContent[i].appendChild(newDiv);

            let orderContentLeft = document.querySelectorAll(".order-content-left");
            newImg = document.createElement("img");
            newImg.src = data[i].attraction[0].image;
            orderContentLeft[i].appendChild(newImg);

            newDiv = document.createElement("div");
            newDiv.className = "order-content-right";
            orderContent[i].appendChild(newDiv);

            let orderContentRight = document.querySelectorAll(".order-content-right")
            newP = document.createElement("p");
            newP.innerHTML = `訂單編號 : ${data[i].product_number}`
            orderContentRight[i].appendChild(newP);

            newP = document.createElement("p");
            newP.innerHTML = `訂購者 : ${data[i].name}`;
            orderContentRight[i].appendChild(newP);

            newP = document.createElement("p");
            newP.innerHTML = `email : ${data[i].email}`;
            orderContentRight[i].appendChild(newP);

            newP = document.createElement("p");
            newP.innerHTML = `電話號碼 : ${data[i].phone}`;
            orderContentRight[i].appendChild(newP);

            newP = document.createElement("p");
            newP.innerHTML = `價格 : ${data[i].price}`;
            orderContentRight[i].appendChild(newP);

            newImg = document.createElement("img");
            newImg.src = "static/images/arrow-down.png";
            newImg.className = "arrow-down-img";
            orderContent[i].appendChild(newImg);
            let arrowDownImg = document.querySelectorAll(".arrow-down-img");

            newDiv = document.createElement("div");
            newDiv.className = "history-order-content";
            content.appendChild(newDiv);
            let historyOrder = document.querySelectorAll(".history-order-content");
            historyOrder[i].style.display = "none";

            
            arrowDownImg[i].addEventListener("click",()=>{
                if(historyOrder[i].style.display === "block"){
                    historyOrder[i].style.display = "none";
                    arrowDownImg[i].src = "/static/images/arrow-down.png";
                    return;
                }
                historyOrder[i].style.display = "block";
                arrowDownImg[i].src = "/static/images/arrow-up.png";
            })
            

            for(let k = 0; k < data[i].attraction.length; k ++){
                
                newDiv = document.createElement("div");
                newDiv.className = "attraction-history-order";
                historyOrder[i].appendChild(newDiv);

                let attractinHistoryOrder = document.querySelectorAll(".attraction-history-order");
                newDiv = document.createElement("div");
                newDiv.className = "attraction-history-order-left";
                attractinHistoryOrder[count].appendChild(newDiv);

                let attractionLeft = document.querySelectorAll(".attraction-history-order-left");
                newDiv = document.createElement("div");
                newDiv.className = "attraction-history-order-right";
                attractinHistoryOrder[count].appendChild(newDiv);

                let attractionRight = document.querySelectorAll(".attraction-history-order-right");
                newImg = document.createElement("img");
                newImg.src = data[i].attraction[k].image;
                attractionLeft[count].appendChild(newImg);

                newP = document.createElement("p");
                newP.innerHTML = `景點名稱 : ${data[i].attraction[k].name}`;
                attractionRight[count].appendChild(newP);

                newP = document.createElement("p");
                newP.innerHTML = `地址 : ${data[i].attraction[k].address}`;
                attractionRight[count].appendChild(newP);

                newP = document.createElement("p");
                newP.innerHTML = `日期 : ${data[i].attraction[k].date}`;
                attractionRight[count].appendChild(newP);

                newP = document.createElement("p");
                newP.innerHTML = `時間 : ${data[i].attraction[k].time}`;
                attractionRight[count].appendChild(newP);
                
                attractinHistoryOrder[count].addEventListener("click",()=>{
                    fetch(`api/attractions?keyword=${data[i].attraction[k].name}`)
                    .then((response)=>{
                        return response.json()
                    })
                    .then((data)=>{
                        let attractionId = data.data[0].id;
                        window.location = `/attraction/${attractionId}`;
                    })
                })
                
                count ++;



            }
        
        }
    })
}


