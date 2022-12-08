let backgroundDarker = document.querySelector(".darker");
let loginContent = document.querySelector(".login-content");
let loginClose = document.querySelector(".login-close");
let signupBtn = document.querySelector(".signup-btn");
let signupClose = document.querySelector(".signup-close");
let hadLoginBtn = document.querySelector(".had-login-btn");
let loginErrorMsg = document.querySelector(".login-error-msg");
let signup = document.querySelector(".signup");
let clickToSignup = document.getElementById("clickToSignup");
let errorMsg = document.querySelector(".error-msg");
let clickToLogin = document.getElementById("clickToLogin");
let loginBtn = document.querySelector(".login-btn");
let login = document.querySelector(".login");
let  username, email, password;


loginClose.addEventListener("click",()=>{
    login.style.display = "none";
    backgroundDarker.style.display = "none";
})

signupBtn.addEventListener("click",()=>{
    login.style.display = "none";
    signup.style.display = "block";
    errorMsg.style.display = "none";
})

signupClose.addEventListener("click",()=>{
    signup.style.display = "none";
    backgroundDarker.style.display = "none";
})

hadLoginBtn.addEventListener("click",()=>{
    loginErrorMsg.style.display = "none";
    signup.style.display = "none";
    login.style.display = "block";
    backgroundDarker.style.display = "block";
})

//確認是否是登入的狀態
fetch("/api/user/auth",{
    method : 'GET',
    headers:{
        'Content-type':'application/json; charset=UTF-8',
    },
})
.then((response)=>{
    return response.json()
})
.then((data)=>{
    if(data["data"] === null){
        loginBtn.style.color = "black";
        loginBtn.innerHTML = "登錄/註冊";
        fetch("/api/user/auth",{
            method : "DELETE",
            headers:{
                'Content-type':'application/json; charset=UTF-8',
            },
        })  
    }
    else{
        loginBtn.style.color = "black";
        loginBtn.innerHTML = "登出系統";
    }
})

//點擊登出系統時登出  點擊登入就登入
loginBtn.addEventListener("click",(e)=>{
    if(loginBtn.innerHTML === "登錄/註冊"){
        loginErrorMsg.style.display = "none";
        login.style.display = "block";
        backgroundDarker.style.display = "block";
    }else{
        fetch("/api/user/auth",{
            method : "DELETE",
            headers:{
                'Content-type':'application/json; charset=UTF-8',
            },
        })
        .then(()=>{
            location.reload();
        })
        
    }
})




clickToSignup.addEventListener("click", ()=>{
    username = document.getElementById("name").value;
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;
    fetch("/api/user",{
        method : 'POST',
        body:JSON.stringify({
            "name" : `${username}`,
            "email" : `${email}`,
            "password" : `${password}`
        }),headers:{
            'Content-type':'application/json; charset=UTF-8',
        },
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        if("ok" in data){
            errorMsg.innerHTML = "註冊成功";
            errorMsg.style.color = "green";
            errorMsg.style.display = "block";
        }
        if("error" in data){
            if(data["error"] === true && data["message"] === "此email已經註冊過了"){
                errorMsg.innerHTML = "此email已經註冊過了";
                errorMsg.style.color = "red";
                errorMsg.style.display = "block";
            }
            else if(data["error"] === true && data["message"] === "伺服器出現錯誤"){
                errorMsg.innerHTML = "伺服器出現錯誤";
                errorMsg.style.color = "red";
                errorMsg.style.display = "block";
            }
        }  
    })
})

clickToLogin.addEventListener("click",()=>{
    email = document.getElementById("loginEmail").value;
    password = document.getElementById("loginPassword").value;
    fetch("/api/user/auth",{
        method : 'PUT',
        body:JSON.stringify({
            "email" : `${email}`,
            "password" : `${password}`
        }),headers:{
            'Content-type':'application/json; charset=UTF-8',
        },
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        if("ok" in data){
            loginErrorMsg.innerHTML = "登入成功";
            loginErrorMsg.style.color = "green";
            loginErrorMsg.style.display = "block";
            location.reload();

        }
        if("error" in data){
            if(data["error"] === true && data["message"] === "帳號或密碼錯誤"){
                loginErrorMsg.innerHTML = "帳號或密碼錯誤";
                loginErrorMsg.style.color = "red";
                loginErrorMsg.style.display = "block";
            }
            else if(data["error"] === true && data["message"] === "伺服器出現錯誤"){
                loginErrorMsg.innerHTML = "伺服器出現錯誤";
                loginErrorMsg.style.color = "red";
                loginErrorMsg.style.display = "block";
            }
        }
        
    })
    
    
    

})
