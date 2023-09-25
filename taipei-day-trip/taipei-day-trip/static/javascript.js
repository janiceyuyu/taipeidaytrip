const page = 0;
let keyword = "";
const attractionUrl = "/api/attractions";
const mrturl="/api/mrts"
let nextPage = 0
let src = `${attractionUrl}?page=${nextPage}&keyword=${keyword}`
fetching = false


window.onload = function getData() {
    fetch(mrturl)
    .then(response => response.json())
    .then(data => {
        const listitemcontainer = document.querySelector('.listitemcontainer');
        listitemcontainer.innerHTML = '';

        if (Array.isArray(data.data)) {
            data.data.forEach(item => {
                const listItem = document.createElement('div');
                listItem.textContent = item;
                listitemcontainer.appendChild(listItem);
                listItem.classList.add('listitem');
            });

            
            const arrowLeftIcon = document.querySelector(".arrow-left-icon");
            const arrowRightIcon = document.querySelector(".arrow-right-icon");
            const listContainer = document.querySelector(".container");
            let scrollDistance = 0; // 初始化滾動距離為0

            // 計算移動距離
            function calculateScrollDistance() {
                const containerWidth = listContainer.offsetWidth;
                const listItemWidth = document.querySelector(".listitem").offsetWidth;
                scrollDistance = Math.floor(containerWidth / 1.1); 
            }

            // 初始化滾動距離
            calculateScrollDistance();

            arrowLeftIcon.addEventListener("click", function () {
                listContainer.scrollTo({
                    left: listContainer.scrollLeft - scrollDistance,
                    behavior: 'smooth',//平滑效果
                });
            });

            arrowRightIcon.addEventListener("click", function () {
                listContainer.scrollTo({
                    left: listContainer.scrollLeft + scrollDistance,
                    behavior: 'smooth',//平滑效果
                });
            });

            // 監聽螢幕大小，調整距離
            window.addEventListener("resize", calculateScrollDistance);
        } else {
            console.log("Data format is not as expected.");
        }
    })
    .catch(error => console.log("Error fetching data:", error));

    //點選捷運站進行搜尋
    const listitemcontainer = document.querySelector(".listitemcontainer");
    listitemcontainer.addEventListener("click", function(event) { 
        if (event.target.classList.contains("listitem")){
            keyword = event.target.textContent;
            //console.log("if 內事件 keyword", keyword)
            
            
        }
            //console.log("if 外事件 keyword:", keyword)
            src = `${attractionUrl}?page=0&keyword=`+keyword
            console.log("src with new keyword:", src)
            observer.observe(target) //加上這個確保不發生搜尋關鍵字後，一片空白的問題
        
            attractionsContainer.innerHTML = '';
            document.querySelector(".search_input").value=keyword

            
          
            }        
    )
    

}


    // 關鍵字搜尋
    const keywordInput = document.querySelector('.search_input');
    const searchButton = document.querySelector('.search-button');
    const attractionsContainer = document.getElementById('attractions');
    
    // 監聽：當點選搜尋
    searchButton.addEventListener('click', searchAttractions);
    
    // 監聽：當按enter
    keywordInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            searchAttractions();
        }
    });
    
    // 搜尋景點函式
    function searchAttractions() {
    const keyword = keywordInput.value.trim(); //trim:去除字符串的開頭和结尾的空格
    console.log("Search keyword:", keyword) //可以成功存到輸入的關鍵字

    src = `${attractionUrl}?page=0&keyword=`+keyword
    console.log("src with new keyword:", src)
    observer.observe(target) //加上這個確保不發生搜尋關鍵字後，一片空白的問題

    attractionsContainer.innerHTML = '';
    
  
    }

const options = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1,
};


let callback = (e) => {
    if(e[0].isIntersecting && fetching == false){
        
        fetching === true
        console.log("Fetch src (expect to see new keyword)", src)// 這裡有正確的keyword
        fetch(src)
            .then((response) => response.json())
            .then((data) => {
                    data.data.forEach((attraction) => {
                    const attractionElement = renderAttraction(attraction);
                    document.getElementById('attractions').appendChild(attractionElement);
                });
                if(data.nextPage !== null)
                {   keyword = keywordInput.value.trim(); //最後直接從這裡拿keyword
                    nextPage = data.nextPage;
                    console.log("new next page after fetch:", nextPage, "keyword:", keyword)
                    src = `${attractionUrl}?page=${nextPage}&keyword=${keyword}`
                    console.log("next src:", src)
                    fetching = false

                }else{
                    console.log("No next page")
                    observer.unobserve(target)
                    nextPage=0
                    console.log("initial nextPage:", nextPage)
                    fetching = false

                    return 
                }
            });
            }else{
                console.log("沒碰到，沒有啟動載入")
            }     
       
    };

  

const observer = new IntersectionObserver(callback, options);
const target = document.querySelector('.footer');

if (target) {
    observer.observe(target);
} else {
    console.error('.footer not found');
}

    
    
// 創建景點的函示
function renderAttraction(attraction) {
    const attractionElement = document.createElement('div');
    attractionElement.classList.add('attraction');
    attractionElement.innerHTML = `
        <a href="/attraction/${attraction.id}">
            <div class="attraction-image">
                <img src="${attraction.images[0]}" alt="${attraction.name}">
            </div>
            <div class="name">${attraction.name}</div>
            <div class="details">
                <div class="detail-mrt">${attraction.mrt}</div>
                <div class="detail-cat">${attraction.category}</div>
            </div>
        </a>
    `;
    return attractionElement;
}



