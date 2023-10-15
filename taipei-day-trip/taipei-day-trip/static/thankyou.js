let apiOrderNumberUrl = "/api/order"
let orderNumber = window.location.href.split('=')[1];
let thankyouTitle = document.getElementById("thankyou-title")
let thankyouContent = document.getElementById("thankyou-content")

function getOrderNumberData(){
    fetch(apiOrderNumberUrl+ "/" + orderNumber, {
        method: 'GET',
        headers: {'Authorization': `Bearer `+ window.localStorage.getItem("token")},
        })
        .then(response => {
            
            // footerStyle.style.paddingBottom="100%"

            if (response.status == 400){
                thankyouTitle.textContent = "訂單號碼錯誤"
                thankyouContent.innerHTML = ''
            } else if (response.status == 500 || response.status == 404){
                thankyouTitle.textContent = "伺服器內部錯誤"
                thankyouContent.innerHTML = ''

            }
            
            return response.json()})
        
}
getOrderNumberData()

let orderNumberText = document.getElementById("order-number-text")
orderNumberText.textContent = orderNumber

footer.style.paddingBottom="100%"