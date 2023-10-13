//設定點選註冊登入功能
const loginbutton=document.querySelector('.item2-text')
const loginbuttonbox=document.querySelector('.item2')
const signupdialog=document.getElementById('signupDialog')
const logindialog=document.getElementById('loginDialog')
const closesignupdialog=document.querySelector('.closeicon')
const closelogindialog=document.querySelector('.closeicon_2')
const signupdialoglogin=document.querySelector('.dialog_text_haveaccount')
const logindialogsignup=document.querySelector('.dialog_text_noaccount')
const signuperrornote=document.getElementById('signuperrornote')
const loginerrornote=document.getElementById('loginerrornote')
const emailrule=/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+\.[a-zA-Z]{2,}$/
let isLoggedIn = false

//設定顯示對話框
loginbutton.addEventListener('click', function() {
    //如果 display 属性的目前值为 'none'，表示元素是隐藏的，那麼將執行 if 中的内容。
    signuperrornote.innerHTML=""
    loginerrornote.innerHTML=""
    if (logindialog.style.display === 'none') {
        logindialog.style.display = 'flex';
    } else {
        logindialog.style.display = 'none';
    }
   
  });
//關閉對話框(註冊)
closesignupdialog.addEventListener('click', function() {
    signupdialog.style.display = 'none';    
})
//關閉對話框(登入)
closelogindialog.addEventListener('click', function() {  
    logindialog.style.display = 'none';
})

//切換對話框(註冊-->登入)
signupdialoglogin.addEventListener('click', function() {
    signuperrornote.innerHTML=""
    signupdialog.style.display = 'none';
    logindialog.style.display = 'flex';
  })
  
//切換對話框(登入-->註冊)
logindialogsignup.addEventListener('click', function() {
    loginerrornote.innerHTML=""
    signupdialog.style.display = 'flex';
    logindialog.style.display = 'none';
  })



//註冊流程
const signupgreenbutton = document.getElementById('signupbutton')
const signupurl="/api/user"

// signupgreenbutton.disabled = true;

signupgreenbutton.addEventListener('click', function() {
    signuperrornote.innerHTML = "";
    const name = document.getElementById('signupname').value;
    const email = document.getElementById('signupemail').value;
    const password = document.getElementById('signuppassword').value;

    console.log("singup input: ", name, email, password)

    if (name === "" || email === "" || password === "") {
        signuperrornote.textContent = "請輸入完整姓名、電子信箱與密碼";
        
    } else if (!emailrule.test(email)) {
        signuperrornote.textContent = "請輸入有效的電子信箱";
       
    } else {
        let signUpdata = { "name": name, "email": email, "password": password };
        fetch(signupurl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(signUpdata)
        })
        .then(response => response.json())
        .then(data => {
            console.log("sign up fetch result:", data.error, data.ok);
           
            if (data.ok) {
                console.log("註冊成功");
                signuperrornote.textContent = "註冊成功！請登入系統";
            } else if (data.error === true) {
                console.log("註冊失敗");
                signuperrornote.textContent = "信箱已被註冊，請使用其他信箱註冊";
            } else {
                console.log("註冊失敗");
                signuperrornote.textContent = "系統錯誤，請稍後再試";
            }
        })
        .catch(error => {
            console.error("註冊時發生錯誤:", error);
            signuperrornote.textContent = "註冊時發生錯誤，請稍後再試";
          
        });
    }
});

//登入流程

const logingreenbutton = document.getElementById('loginbutton');
const loginurl = "/api/user/auth";

logingreenbutton.addEventListener('click', function() {
    loginerrornote.innerHTML = "";
    const email = document.getElementById('loginemail').value;
    const password = document.getElementById('loginpassword').value;

    if (email === "" || password === "") {
        loginerrornote.textContent = "請輸入電子信箱與密碼";
    } else {
        let logindata = { "email": email, "password": password };
        console.log(JSON.stringify(logindata))

        fetch(loginurl, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(logindata)
        })
        .then(response => {
            if (!response.ok) {
                loginerrornote.textContent = "電子信箱或密碼輸入錯誤";
                console.log(data.error, data.message);
            }
            return response.json();
        })
        .then(data => {
            if (data.token) {
                window.localStorage.setItem("token", data.token);
                logindialog.style.display = 'none';
                location.reload();
            } 
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
});

window.onload = function() {
    checklogin();
}

function checklogin() {
    fetch(loginurl, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ` + window.localStorage.getItem("token") },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data !== null) {
            logout();
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function logout() {
    loginbutton.style.display = "none";
    let logout = document.createElement("div");
    logout.classList.add("nav-logout-button");
    logout.textContent = "登出系統";

    logout.addEventListener('click', function() {
        localStorage.clear();
        location.reload();
    });
    loginbuttonbox.appendChild(logout);
}
   








