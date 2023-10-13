let id = window.location.pathname.split('/')[2];
console.log(id)
const idurl=`/api/attraction/${id}`;
console.log(idurl)
let imagesUrl = []
let bookingurl= "/api/booking"
let booking_button=document.getElementById('booking_button')


fetch(idurl)
.then(response => response.json())
.then(data => {
    const name = document.querySelector('.name');
    name.textContent=data.data.name;
    //console.log(data.data);
    const detail_cat = document.querySelector('.detail-cat');
    detail_cat.textContent=data.data.category;
    //console.log(detail_cat);
    const detail_mrt = document.querySelector('.detail-mrt');
    detail_mrt.textContent=data.data.mrt;
    //console.log(detail_mrt);
    const infors_details = document.querySelector('.infors-details');
    infors_details.textContent=data.data.description;
    //console.log(infors_details);
    const address_1 = document.querySelector('.address-1');
    address_1.textContent=data.data.address;
    //console.log(address_1);
    const transport_1 = document.querySelector('.transport-1');
    transport_1.textContent=data.data.transport;
    //console.log(transport_1);
    // console.log(data.data.images) // 預期的陣列型態

    imagesUrl=data.data.images 
    // console.log("imagesUrl: ",imagesUrl)
    
    showImages();


})

//顯示圖片
const pictureCurrent = document.querySelector('.picture-current');
const dotsbox = document.getElementById("dots");
const leftButton = document.getElementById("left_arrow");
const rightButton = document.getElementById("right_arrow");
let currentIndex = 0 //當前圖片號碼，一開始是零

function showImages(){
  pictureCurrent.innerHTML=""
  imagesUrl.forEach((imageUrl, index) => {
      console.log(imageUrl, "index: ", index)
      const slide = document.createElement("div")
      slide.classList.add("slide-div")
      if (index === currentIndex){
          slide.classList.add("active");
      }
      const image = document.createElement('img');
      image.src = imageUrl;
      image.className = 'custom-image';
      image.classList.add('custom-image');
      slide.appendChild(image)
      pictureCurrent.appendChild(slide);
      // console.log(pictureCurrent)
    });
    
    updateIndicator()

  }

  function updateIndicator(){
    dotsbox.innerHTML=""
    imagesUrl.forEach((_, index) => {
        const dot = document.createElement("span")
        dot.classList.add("indicator-dot")
        if (index === currentIndex){
            dot.classList.add("active")
        }
        dotsbox.appendChild(dot)


    })
}

function prevSlide(){
    if (currentIndex > 0){
        currentIndex --;
    }else{
        currentIndex = imagesUrl.length -1
    }
    showImages()
}

function nextSlide(){
    if (currentIndex < imagesUrl.length-1){
        currentIndex ++;
    }else{
        currentIndex = 0;
    }

    showImages()
}

 
leftButton.onclick=function(){
  prevSlide()
  console.log("pressed prev")
};
rightButton.onclick=function(){
  nextSlide()
  console.log("pressed next")

};








//點選上下半天對應價錢

//事件監聽
const button1 = document.querySelector('#price_2000');
const button2 = document.querySelector('#price_2500');
const price1 = document.querySelector('.price_1');
const price2 = document.querySelector('.price_2');

button1.addEventListener('click', function() {
    price1.style.display = 'block';
    price2.style.display = 'none';
  });

button2.addEventListener('click', function() {
    // 顯示 price2，隱藏 price1
    price2.style.display = 'block';
    price1.style.display = 'none';
  });

//預訂新的行程
let priceInt = ""
let selectedTime=""    

booking_button.addEventListener('click',function(){
    checklogin({checkBookingSignin: true})
})
function addBookingOrder(){
    let selectDate = document.querySelector('.customDatePicker').value
    if (selectDate == ""){
        alert("請選擇日期")
    }else{ 
        console.log(selectDate)

    let selectedTime = document.querySelector('input[name="daytime"]:checked').value;  
    console.log(selectedTime);
        
      
    const button1 = document.querySelector('#price_2000');
    const button2 = document.querySelector('#price_2500');


    let selectedPrice = "";

    if (button1.checked) {
        selectedPrice =  document.getElementById("2000").textContent
    } else if (button2.checked) {
        selectedPrice =  document.getElementById("2500").textContent
    }
    const priceMatches = selectedPrice.match(/\d+/);

    if (priceMatches && priceMatches.length > 0) {
        // 將匹配到的數字轉換為整數
        priceInt = parseInt(priceMatches[0], 10);
        console.log("選擇的導覽費用：" + priceInt + " 元");
    } else {
        alert("請選擇時間");
    }
        
  
    let attractionId = id
    
    let bookingData = {"attractionID": attractionId, "date": selectDate, "time": selectedTime, "price": priceInt}
    console.log(bookingData)
    
    fetch(bookingurl, {
        method: 'POST',
        headers: {'Authorization': `Bearer `+ window.localStorage.getItem("token"), 'Content-Type': 'application/json'},
        body: JSON.stringify(bookingData)
        })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        location.href = "/booking"
    })
    }
}
