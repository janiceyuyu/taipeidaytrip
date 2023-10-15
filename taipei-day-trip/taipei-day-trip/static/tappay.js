let apiOrderUrl = "/api/orders"
let thankyouOrderNumber = ''

TPDirect.setupSDK(
    137431,
    "app_Anq4TqO8JqrTNBoDq8XYkrpKSXjq94q1LSR4t1rfLs9dc3VOHuDK3zOWHwip",
    "sandbox"
  );



  let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: '後三碼'
    }
}
TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        'input.ccv': {
        },
        'input.expiration-date': {
        },
        'input.card-number': {
        },
        ':focus': {
            'color': 'black'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
        
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6, 
        endIndex: 11
    }
})
const confirmbutton=document.querySelector('.confirm-button')
TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        confirmbutton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        confirmbutton.setAttribute('disabled', true)
    }


})


let prime = ''
let bookingContactName = document.getElementById("contactname")
let bookingContactEmail = document.getElementById("contactemail")
let bookingContactPhone = document.getElementById("contactphone")

confirmbutton.addEventListener("click", function(event){


    event.preventDefault()


    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('請完整填寫所有欄位')
        return
    }

    // Get prime
    async function getPrimeAsync() {
        return new Promise((resolve, reject) => {
            TPDirect.card.getPrime((result) => {
                if (result.status !== 0) {
                    reject('get prime error ' + result.msg);
                } else {
                    resolve(result.card.prime);
                }
            });
        });
        
    }
    async function sendPrimeData() {
        try {
            const prime = await getPrimeAsync();
    
            const orderData = {
                "prime": prime,
                "order": {
                    "price": price,
                    "trip": {
                        "attraction": {
                            "id": bookingAttractionId,
                            "name": bookingSpotName,
                            "address": bookingaddress,
                            "image": bookingimageUrl
                        },
                        "date": date,
                        "time": time
                    },
                    "contact": {
                        "name": bookingContactName.value,
                        "email": bookingContactEmail.value,
                        "phone": bookingContactPhone.value
                    }
                }
            };
    
            console.log("orderData", orderData);
    
            const response = await fetch(apiOrderUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ` + window.localStorage.getItem("token"),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderData)
            });
    
            const paymentData = await response.json();
            console.log(paymentData.data.number, paymentData);

            if (paymentData.data.payment.status != 0){
                alert('付款失敗，請重新付款。error code: '+ paymentData.data.payment.status)
            }

            // 要把'?number=' + 訂單編號

            thankyouOrderNumber = await paymentData.data.number
            console.log("tks order number:", thankyouOrderNumber)
    
            // 在這裡可以處理伺服器的回應
            


            location.href = "/thankyou?number=" + thankyouOrderNumber;
            deleteBooking();
        } catch (error) {
            console.error(error);
        }
    }
    
    // 呼叫主函數
    sendPrimeData();

    


})


function deleteBooking(){
    fetch('/api/booking', {
        method: 'DELETE',
        headers: {'Authorization': `Bearer `+ window.localStorage.getItem("token")},
        })
    .then(response => response.json())
    
}
    