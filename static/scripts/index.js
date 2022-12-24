const bottom = document.querySelector(".bottom");
const search = document.querySelector(".icon-search-bg");
const message = document.querySelector(".message");
let input = document.getElementById("title-input");
let categories = document.getElementById("categories");
let child = document.querySelector(".child");
let content = document.getElementById("content");
let newP, textNode, dataContent, contentBaby, newChild, username, email, password;
let pages = 12;
let firstChange = false;
let clickEvent = false;
let prevSearch = "";
let url = "/api/categories";

window.onload = function(){
    getHomePage();
}
fetch(url)
.then((response)=>{
    return response.json()
})
.then((data)=>{
    let catNum = 1;
    data = data["data"];
    for(let i = 0; i < data.length; i++){
        newP = document.createElement("p");
        textNode = document.createTextNode(data[i]);
        newP.appendChild(textNode);
        newP.className = `cat${catNum}`;
        categories.appendChild(newP);
        addClickEvent(catNum);
        catNum ++;
    }
})





//點擊input，把索引顯示在input
input.addEventListener("click",function(e){
    stopFunc(e);
    categories.style.visibility = "visible";
});

document.addEventListener("click",function(e){
    categories.style.visibility = "hidden"

})
function stopFunc(e) { 
    e.stopPropagation ? e.stopPropagation() : e.cancelBubble = true;
}




//點擊搜尋
search.addEventListener("click",function(){
    message.style.display = "none";
    clickEvent = true;
    let inputValue = input.value;
    if(inputValue === prevSearch && inputValue != ""){
        return;
    }
    let removeChild = document.querySelectorAll(".child");
    for(let i = 0; i < removeChild.length; i++){
        content.removeChild(removeChild[i]); 
    }
    getHomePage(inputValue);
    prevSearch = inputValue;
})

titleLeftFont.addEventListener("click",function(){
    window.location = "/";
    clickEvent = false;
})



//取得分頁
let loading = false;
let pageEnd = false;
let nextPage;
let options = {
    threshold: 0.1,
}

//IntersectionObserver
function getHomePage(keyword=""){
    message.style.display = "none";
    firstChange = false;
    pageEnd = false;
    nextPage = 0;
    let observer = new IntersectionObserver((entries) =>{
        for (let entry of entries){
            if(entry.isIntersecting){
                if(pageEnd != true && loading === false){
                    if(keyword !== "" && clickEvent === true){
                        url = `/api/attractions?page=${nextPage}&keyword=${keyword}`;
                        loadAttractions(url,nextPage)
                            .catch(()=>{
                                message.style.display = "block";
                            })  
                    }
                    else if(keyword === "" && clickEvent === false ){
                        url = `/api/attractions?page=${nextPage}`;
                        loadAttractions(url,nextPage);
                    }  
                }
                if(pageEnd === true){
                    observer.unobserve(bottom);
                }   
            }
        }
    },options);
    observer.observe(bottom);
}



async function loadAttractions(url,page){
    loading = true;
    let response = await fetch(url);
    let data = await response.json();
    
    dataContent = data["data"];
    
    nextPage = data["nextPage"];        
    await test(dataContent);
    function test (dataContent){
        if(dataContent.length === 0 && data["nextPage"] === null){
            pageEnd = true;
            loading = false;
            return Promise.reject();
        }
        for(let i = 0; i < dataContent.length; i++){
            if(firstChange === false){
                createChild();
                let titleFont = document.querySelectorAll(".title-font");
                let leftFont = document.querySelectorAll(".left-p");
                let rightFont = document.querySelectorAll(".right-p");
                let contentPC = document.querySelectorAll(".content-pc");
                titleFont[page*pages + i].innerHTML = dataContent[i]["name"];
                leftFont[page*pages + i].innerHTML = dataContent[i]["mrt"];
                rightFont[page*pages + i].innerHTML = dataContent[i]["category"];
                contentPC[page*pages + i].src = dataContent[i]["images"][0];
                firstChange = true;
                child.addEventListener("click",function(){
                    let attractionUrl = `/api/attractions?page=0&keyword=${titleFont[page*pages + i].innerHTML}`;
                    getData(attractionUrl);
                })
                continue;
            }
            let newChild = child.cloneNode(true);

            
            
            content.appendChild(newChild);
            let titleFont = document.querySelectorAll(".title-font");
            let leftFont = document.querySelectorAll(".left-p");
            let rightFont = document.querySelectorAll(".right-p");
            let contentPC = document.querySelectorAll(".content-pc");
            contentPC[page*pages + i].src = "";
            titleFont[page*pages + i].innerHTML = dataContent[i]["name"];
            leftFont[page*pages + i].innerHTML = dataContent[i]["mrt"];
            rightFont[page*pages + i].innerHTML = dataContent[i]["category"];
            contentPC[page*pages + i].src = dataContent[i]["images"][0];
            newChild.addEventListener("click",function(){
                let attractionUrl = `/api/attractions?page=0&keyword=${titleFont[page*pages + i].innerHTML}`;
                getData(attractionUrl);
            })
        }
        
        if(data.nextPage === null){ //調整flex最後一排留下的縫隙，讓物件靠左
            pageEnd = true;
            let count = document.querySelectorAll(".title-font").length;
            let mod = count % 4;
            if(window.innerWidth > 600){
                if(mod != 0){
                    for(let i = 0; i < 4 - mod; i++){
                        newChild = child.cloneNode(true);
                        content.appendChild(newChild);
                    }
                    for(let i = 0; i < 4 - mod; i++){
                        count =  document.querySelectorAll(".title-font").length;
                        let childCount = document.querySelectorAll(".child");

                        childCount[count - 1 - i].style.visibility = "hidden";
                    }
                
                }
            }
        }  
        loading = false;
    }  
}


//點擊圖片轉址
async function getData(url){  
    let response = await fetch(url);
    let data = await response.json();
    window.location = `/attraction/${data["data"][0]["id"]}`;
}

//點擊categories時，自動填入input搜尋框
function addClickEvent(catNum){
    let category = document.querySelector(`.cat${catNum}`);
    category.addEventListener("click",function(){
        input.value = category.innerHTML;
    })
}


// 創建第一個child
function createChild(){
    let newDiv = document.createElement("div");
    newDiv.className = "child";
    content.appendChild(newDiv);
    child = document.querySelector(".child");
    let newImg = document.createElement("img");
    newImg.className = "content-pc";
    child.appendChild(newImg);
    let newP = document.createElement("p");
    newP.className= "title-font";
    child.appendChild(newP);
    newDiv = document.createElement("div");
    newDiv.className = "content-baby";
    child.appendChild(newDiv);
    newP = document.createElement("p");
    newP.className = "left-p";
    contentBaby = document.querySelector(".content-baby");
    contentBaby.appendChild(newP);
    newP = document.createElement("p");
    newP.className = "right-p";
    contentBaby.appendChild(newP);
}