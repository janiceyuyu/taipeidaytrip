let bookingSchedule = document.getElementById("bookingschedule")

let welcomeTitleName = document.getElementById("username")

let welcomeUsername = "" 
let userContactName = document.getElementById("contactname")
let userContactEmail = document.getElementById("contactemail")

let bookingSpotNameText = document.getElementById("spotname")
let bookingDate = document.getElementById("date")
let bookingTime = document.getElementById("time")
let bookingPrice = document.getElementById("cost")
let bookingAddressText = document.getElementById("address")
let bookingSpotImageContainer = document.getElementById("bookingpicture")
let totalPrice = document.getElementById("totalcost")

let section=document.getElementById("section")
let line2=document.getElementById("line2")
let contactform=document.getElementById("contactform")
let line3=document.getElementById("line3")
let payment=document.getElementById("payment")
let line4=document.getElementById("line4")
let confirm_1=document.getElementById("confirm")

let deleteButton = document.querySelector(".deleteicon")

let footer = document.querySelector(".footer");

//點擊行程預定事件
bookingSchedule.addEventListener('click', function() {
    bookingchecklogin()
    
})
//執行確認是否有登入
function bookingchecklogin() {
    fetch(loginurl, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ` + window.localStorage.getItem("token") },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.id){
            location.href = "/booking"
        }else {
            signupdialog.style.display = 'none';
            logindialog.style.display = 'flex';
        }
  
    })
}
//如果已登入要取得會員資料
getmemberdata()
function getmemberdata(){
    fetch(loginurl, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ` + window.localStorage.getItem("token") },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        welcomeUsername=data.name 
        welcomeTitleName.textContent = welcomeUsername
        userContactName.value = welcomeUsername
        
        let userEmail = data.email
        userContactEmail.value = userEmail


    })

    getbookingdata()
}

deleteButton.addEventListener('click', function(){
        
    fetch(bookingurl, {
        method: 'DELETE',
        headers: {'Authorization': `Bearer `+ window.localStorage.getItem("token")},
        })
    .then(response => response.json())
    .then(data => {
        console.log("刪除API的data",data)
        getbookingdata()

    })
})

//取得預定行程的資料
function getbookingdata(){
    fetch(bookingurl, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ` + window.localStorage.getItem("token") },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.data){
        console.log(data.data.attraction)
        let bookingimageUrl = data.data.attraction.images
        //console.log(bookingimageUrl)
        let bookingSpotName = data.data.attraction.name
        //console.log(bookingSpotName)
        let bookingaddress = data.data.attraction.address
        //console.log(bookingaddress)
        let date = data.data.date
        //console.log(date)
        let time = data.data.time
        if (time=="morning"){
            time = "上午 9 點至下午 4 點"
        }else if(time=="afternoon"){
            time = "下午 3 點至晚上 9 點"
        }
        //console.log(time)
        let price = data.data.price
        //console.log(price)
        bookingSpotNameText.textContent=bookingSpotName
        bookingDate.textContent = date
        bookingTime.textContent = time
        bookingPrice.textContent = price
        totalPrice.textContent = price
        bookingAddressText.textContent = bookingaddress
        
        let img = document.createElement("img")
        img.src = bookingimageUrl
        img.classList.add("bookingpicture")
        bookingSpotImageContainer.appendChild(img)

        }else{
        
 
            // console.log("刪除之後的:",data.data.attraction)
            section.innerHTML = ""
            contactform.style.display = "none";
            payment.style.display = "none";
            confirm_1.style.display = "none";
            line2.style.display = "none";
            line3.style.display = "none";
            line4.style.display = "none";

    
            let nullDataText = document.createElement("div")
            nullDataText.classList.add("nullDataText")
            nullDataText.textContent = "目前沒有任何待預訂的行程"
            section.appendChild(nullDataText)
            
            footer.style.paddingBottom="100%"

        }


})}
