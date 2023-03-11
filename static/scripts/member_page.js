const idName = document.querySelector(".id-name");
const headshot = document.querySelector(".headshot");
const nameInput = document.querySelector(".name-input");
const emailInput = document.querySelector(".email-input");
const username = document.querySelector(".username");
const email = document.querySelector(".user-email");
const cancelBtn = document.querySelector(".cancel-btn");
const imgFileBtn = document.querySelector(".img-file");
const uploadBtn = document.querySelector(".upload-pc-btn");
const messsage = document.querySelector(".message");
const penBtn = document.querySelector(".pen-btn");
const changeNameBtn = document.querySelector(".change-name-btn");
const changeEmailBtn = document.querySelector(".change-email-btn");
const okNameBtn = document.querySelector(".ok-name-btn");
const okEmailBtn = document.querySelector(".ok-email-btn");
const errorMsg = document.querySelector(".update-error-msg");
const cancelImgBtn = document.querySelector(".cancel-img-btn");
let originSrc;
let pcChange = false;


//檢查是否曾經有上傳過大頭貼
fetch("/check_is_upload_headshot")
    .then((data) => {
        return data.json()
    })
    .then((response) => {
        if ("ok" in response) {
            headshot.src = `./static/images/${idName.innerHTML}.png`
        }
        else if ("error" in response) {
            headshot.src = './static/images/default_headshot.png'
        }
    })


//點擊修改圖片
penBtn.addEventListener("click", () => {
    imgFileBtn.style.display = "block";
    uploadBtn.style.display = "block";
    cancelImgBtn.style.display = "block";

})

changeNameBtn.addEventListener("click", () => {
    nameInput.style.display = "block";
    nameInput.value = username.innerHTML;
    username.style.display = "none";
    okNameBtn.style.display = "block";
    changeNameBtn.style.display = "none";
    cancelBtn.style.display = "block";
})

changeEmailBtn.addEventListener("click", () => {
    emailInput.style.display = "block";
    emailInput.value = email.innerHTML;
    email.style.display = "none";
    okEmailBtn.style.display = "block";
    changeEmailBtn.style.display = "none";
    cancelBtn.style.display = "block";
})

cancelBtn.addEventListener("click", () => {
    okNameBtn.style.display = "none";
    changeNameBtn.style.display = "block";
    username.style.display = "block";
    nameInput.style.display = "none";
    okEmailBtn.style.display = "none";
    changeEmailBtn.style.display = "block";
    email.style.display = "block";
    emailInput.style.display = "none";
    cancellErrorMsg(errorMsg);
    cancelBtn.style.display = "none";
})

cancelImgBtn.addEventListener("click", () => {
    imgFileBtn.style.display = "none";
    uploadBtn.style.display = "none";
    cancelImgBtn.style.display = "none";
    if (pcChange === true) {
        headshot.src = originSrc;
    }


})

okNameBtn.addEventListener("click", () => {
    if (nameInput.value === "") {
        showErrorMsg(errorMsg, "⚠不可為空", "red", "block");
        return;
    }
    //更新token 和 更新資料庫的name
    fetch("/change_profile", {
        method: 'POST',
        body: JSON.stringify({
            "name": nameInput.value,
        }), headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
        .then((data) => {
            return data.json()
        })
        .then((response) => {
            console.log(response);
            if ("ok" in response) {
                okNameBtn.style.display = "none";
                changeNameBtn.style.display = "block";
                username.style.display = "block";
                username.innerHTML = nameInput.value;
                nameInput.style.display = "none";
                fetch("/update_token", {
                    method: 'POST',
                })
                cancelBtn.style.display = "none";
                cancellErrorMsg(errorMsg);

            }
        })
})


okEmailBtn.addEventListener("click", () => {
    let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
    if (emailInput.value === "") {
        showErrorMsg(errorMsg, "⚠不可為空", "red", "block");
        return;
    }
    if (emailInput.value.search(emailRule) != -1) {
        //更新token 和 更新資料庫的email
        showErrorMsg(errorMsg, "", "black", "none");
        fetch("/change_profile", {
            method: 'POST',
            body: JSON.stringify({
                "email": emailInput.value,
            }), headers: {
                'Content-type': 'application/json; charset=UTF-8',
            },
        })
            .then((data) => {
                return data.json()
            })
            .then((response) => {
                console.log(response);
                if ("ok" in response) {
                    okEmailBtn.style.display = "none";
                    changeEmailBtn.style.display = "block";
                    email.style.display = "block";
                    email.innerHTML = emailInput.value;
                    emailInput.style.display = "none";
                    fetch("/update_token", {
                        method: 'POST',
                    })
                    cancelBtn.style.display = "none";
                    cancellErrorMsg(errorMsg);
                } else if ("error" in response) {
                    if (response.message === "email已經被註冊過了") {
                        showErrorMsg(errorMsg, "⚠email已經被註冊過了", "red", "block");
                    }
                    else if (response.message === "內部伺服器發生錯誤") {
                        showErrorMsg(errorMsg, "⚠內部伺服器發生錯誤", "red", "block");
                    }
                }
            })
    } else {
        showErrorMsg(errorMsg, "⚠email格式錯誤", "red", "block");
        return;
    }


})


//預覽大頭貼
imgFileBtn.addEventListener("change", openFile)

function openFile(event) {
    var input = event.target; //取得上傳檔案
    var reader = new FileReader(); //建立FileReader物件

    reader.readAsDataURL(input.files[0]); //以.readAsDataURL將上傳檔案轉換為base64字串
    originSrc = headshot.src;
    pcChange = true;
    reader.onload = function () { //FileReader取得上傳檔案後執行以下內容
        var dataURL = reader.result; //設定變數dataURL為上傳圖檔的base64字串
        headshot.src = dataURL //將img的src設定為dataURL並顯示
        headshot.show();
    };
}

function showErrorMsg(object, message, color, status) {
    object.innerHTML = message;
    object.style.color = color;
    object.style.display = status;
}

function cancellErrorMsg(object) {
    object.style.display = "none";
}