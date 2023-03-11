const backgroundDarker = document.querySelector(".darker");
const loginContent = document.querySelector(".login-content");
const loginClose = document.querySelector(".login-close");
const signupBtn = document.querySelector(".signup-btn");
const signupClose = document.querySelector(".signup-close");
const hadLoginBtn = document.querySelector(".had-login-btn");
const clickToLogin = document.getElementById("clickToLogin");
const order = document.querySelector(".order");
const titleFont = document.getElementById("titleLeftFont");
const clickToSignup = document.getElementById("clickToSignup");
const signup = document.querySelector(".signup");
const login = document.querySelector(".login");
const hamburger = document.querySelector(".hamburger");
const historyOrder = document.querySelector(".history-order");
const memberPage = document.querySelector(".member-page");
const shoppingCartImg = document.querySelector(".shopping-cart-container");
const productCount = document.querySelector(".product-count");
const headshotContainer = document.querySelector(".member-headshot-container");
const memberHeadshot = document.querySelector(".member-headshot");
const loginErrorMsg = document.querySelector(".login-error-msg");
const errorMsg = document.querySelector(".error-msg");
const loginBtn = document.querySelector(".login-btn");

let isLogin = false;
let username, email, password;




//確認是否是登入的狀態
fetch("/api/user/auth", {
    method: 'GET',
    headers: {
        'Content-type': 'application/json; charset=UTF-8',
    },
})
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data["data"] === null) {
            loginBtn.style.color = "black";
            loginBtn.innerHTML = "登錄/註冊";
            productCount.style.display = "none";
            fetch("/api/user/auth", {
                method: "DELETE",
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })

        }
        else {
            loginBtn.style.color = "black";
            loginBtn.innerHTML = "登出";
            isLogin = true;

            if (window.innerWidth > 600) {
                memberHeadshot.style.display = "block";
            }

            memberPage.style.display = "none";
            fetch("/check_is_upload_headshot")
                .then((data) => {
                    return data.json()
                })
                .then((response) => {
                    if ("ok" in response) {
                        memberHeadshot.src = `/static/images/${response.id}.png`;
                    } else {
                        memberHeadshot.src = `/static/images/default_headshot.png`;
                    }
                })
        }
    })

//取得購物車裡面訂單的數量
fetch("/api/booking")
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        productCount.innerHTML = data.data.length;
    })


//點擊navbar<台北一日遊>跳回首頁
titleFont.addEventListener("click", function () {
    window.location = "/";
})

//登入的叉叉
loginClose.addEventListener("click", () => {
    login.style.display = "none";
    backgroundDarker.style.display = "none";
})

//註冊的叉叉
signupClose.addEventListener("click", () => {
    signup.style.display = "none";
    backgroundDarker.style.display = "none";
})



signupBtn.addEventListener("click", () => {
    login.style.display = "none";
    signup.style.display = "block";
    errorMsg.style.display = "none";
})

shoppingCartImg.addEventListener("click", () => {
    if (isLogin === true) {
        window.location = "/booking";
    } else {
        LoginPopup();
    }

})

hadLoginBtn.addEventListener("click", () => {
    loginErrorMsg.style.display = "none";
    signup.style.display = "none";
    login.style.display = "block";
    backgroundDarker.style.display = "block";
})

//點擊歷史訂單
historyOrder.addEventListener("click", () => {
    if (isLogin === true) {
        window.location = "/history_order";
    } else {
        LoginPopup();

    }
})

memberHeadshot.addEventListener("click", () => {
    if (isLogin === true) {
        window.location = "/member_page"
    } else {
        LoginPopup();
    }
})

//點擊預定行程
// order.addEventListener("click",()=>{
//     if(isLogin === true){
//         window.location = "/booking";
//     }else{
//         LoginPopup();

//     }
// })

//點擊會員頁面
memberPage.addEventListener("click", () => {
    if (isLogin === true) {
        window.location = "/member_page";
    } else {
        LoginPopup();
    }
})

//點擊登出系統時登出  點擊登入就登入
loginBtn.addEventListener("click", (e) => {
    if (loginBtn.innerHTML === "登錄/註冊") {
        loginErrorMsg.style.display = "none";
        login.style.display = "block";
        backgroundDarker.style.display = "block";
    } else {
        fetch("/api/user/auth", {
            method: "DELETE",
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            },
        })
            .then(() => {
                location.reload();

            })
    }
})

//點擊註冊新帳號
clickToSignup.addEventListener("click", () => {
    username = document.getElementById("name").value;
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;
    let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
    if (username === "" || email === "" || password === "") {
        showErrorMsg(errorMsg, "⚠任一項不可為空", "red", "block");
        return;
    }
    if (email.search(emailRule) != -1) {
        registerNewAccount(username, email, password);
    } else {
        showErrorMsg(errorMsg, "⚠email格式錯誤", "red", "block");
        return;
    }

    registerNewAccount(username, email, password);
})

//點擊登錄帳號
clickToLogin.addEventListener("click", () => {
    email = document.getElementById("loginEmail").value;
    password = document.getElementById("loginPassword").value;
    fetch("/api/user/auth", {
        method: 'PUT',
        body: JSON.stringify({
            "email": `${email}`,
            "password": `${password}`
        }), headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if ("ok" in data) {
                showErrorMsg(loginErrorMsg, "登入成功", "green", "block")
                location.reload();
            }
            if ("error" in data) {
                if (data["error"] === true && data["message"] === "帳號或密碼錯誤") {
                    showErrorMsg(loginErrorMsg, "帳號或密碼錯誤", "red", "block");
                }
                else if (data["error"] === true && data["message"] === "伺服器出現錯誤") {
                    showErrorMsg(loginErrorMsg, "伺服器出現錯誤", "red", "block");
                }
            }

        })
})

//手機板點擊漢堡圖
hamburger.addEventListener("click", (e) => {
    if (isLogin === true) {
        if (loginBtn.style.display === "block") {
            loginBtn.style.display = "none";
            shoppingCartImg.style.visibility = "hidden";
            historyOrder.style.display = "none";
            memberHeadshot.style.display = "none";
            headshotContainer.style.display = "none";

            return;
        }
        stopFunc(e);
        loginBtn.style.display = "block";
        shoppingCartImg.style.visibility = "visible";
        historyOrder.style.display = "block";
        memberHeadshot.style.display = "block";
        headshotContainer.style.display = "block";
    } else {
        if (loginBtn.style.display === "block") {
            loginBtn.style.display = "none";
            shoppingCartImg.style.visibility = "hidden";
            historyOrder.style.display = "none";
            memberPage.style.display = "none";

            return;
        }
        stopFunc(e);
        loginBtn.style.display = "block";
        shoppingCartImg.style.visibility = "visible";
        historyOrder.style.display = "block";
        memberPage.style.display = "block";
    }


})

document.addEventListener("click", function (e) {
    if (isLogin === true) {
        if (window.innerWidth < 600) {
            loginBtn.style.display = "none";
            shoppingCartImg.style.visibility = "hidden";
            historyOrder.style.display = "none";
            memberHeadshot.style.display = "none";
            headshotContainer.style.display = "none";
        }
    } else {
        if (window.innerWidth < 600) {
            loginBtn.style.display = "none";
            shoppingCartImg.style.visibility = "hidden";
            historyOrder.style.display = "none";
            memberPage.style.display = "none";
        }
    }

})



function stopFunc(e) {
    e.stopPropagation ? e.stopPropagation() : e.cancelBubble = true;
}

function LoginPopup() {
    loginErrorMsg.style.display = "none";
    login.style.display = "block";
    backgroundDarker.style.display = "block";
}

function registerNewAccount(username, email, password) {
    fetch("/api/user", {
        method: 'POST',
        body: JSON.stringify({
            "name": `${username}`,
            "email": `${email}`,
            "password": `${password}`
        }), headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if ("ok" in data) {
                showErrorMsg(errorMsg, "註冊成功", "green", "block");
            }
            if ("error" in data) {
                if (data["error"] === true && data["message"] === "此email已經註冊過了") {
                    showErrorMsg(errorMsg, "⚠此email已經註冊過了", "red", "block");
                } else if (data["error"] === true && data["message"] === "任一項不可為空") {
                    showErrorMsg(errorMsg, "⚠任一項不可為空", "red", "block");
                } else if (data["error"] === true && data["message"] === "email格式錯誤") {
                    showErrorMsg(errorMsg, "⚠email格式錯誤", "red", "block");
                }
                else if (data["error"] === true && data["message"] === "伺服器出現錯誤") {
                    showErrorMsg(errorMsg, "⚠伺服器出現錯誤", "red", "block");
                }

            }
        })
}

function showErrorMsg(object, message, color, status) {
    object.innerHTML = message;
    object.style.color = color;
    object.style.display = status;
}

