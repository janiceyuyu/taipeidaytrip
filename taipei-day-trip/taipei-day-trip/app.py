from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector



# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

#API取得景點資料列表----------------------------------------------
@app.route("/api/attractions", methods=["GET"])
def apiattractions():
    page = int(request.args.get("page", 0))  
    per_page = 12  # 每頁顯示的資料筆數
    keyword = request.args.get("keyword")
    
    try:
        # 連線資料庫
        con = mysql.connector.connect(  
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4"
        )
        cursor = con.cursor()
        
        if keyword:
            # 執行SQL指令，去資料庫裏面查詢
            query = "SELECT id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions WHERE mrt = %s OR name LIKE %s"
            keyword_pattern = f"%{keyword}%"
            cursor.execute(query, (keyword, keyword_pattern))
            
            # 將查詢到的資料存放在taipeidaytrip的變數中
            taipeidaytrip = cursor.fetchall()
        else:
            # 如果未提供關鍵字，則檢索所有資料
            query = "SELECT id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions"
            cursor.execute(query)
            
            taipeidaytrip = cursor.fetchall()

        # 關閉游標和連線
        cursor.close()
        con.close()
        
        total_records = len(taipeidaytrip) # 計算資料總長度
        total_pages = (total_records // per_page) # 計算頁數

        if total_records % per_page > 0:
            total_pages += 1

        start_idx = page  * per_page
        end_idx = start_idx + per_page
        paginated_data = taipeidaytrip[start_idx:end_idx]

        # 檢查是否為最後一頁
        is_last_page = page == total_pages - 1

        # 檢查是否有足夠的數據
        enough_data = total_records >= per_page  # 使用 >= 來檢查是否有足夠的數據

        # 設定 next_page 的值
        if is_last_page and not enough_data:  # 只有在是最後一頁且不足 12 筆資料時設定 next_page 為 None
            next_page = None
        else:
            next_page = page + 1

        if total_records - (page * per_page) < per_page:
            next_page = None

        if taipeidaytrip:
            attractions = []
            for row in paginated_data:  # 使用分頁後的資料
                # 將圖片URL轉換為Python列表
                images = json.loads(row[9])

                # 移除圖片URL中的反斜杠符號
                cleaned_images = [image.replace("\\", "") for image in images]

                attraction = {
                    "id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "description": row[3],
                    "address": row[4],
                    "transport": row[5],
                    "mrt": row[6],
                    "lat": float(row[7]),
                    "lng": float(row[8]),
                    "images": cleaned_images  # 使用處理後的圖片URL列表
                }
                attractions.append(attraction)

            response_data = {
                "nextPage": next_page,
                "data": attractions
            }
            return json.dumps(response_data, ensure_ascii=False), 200
        else:
            return json.dumps({"error": True}, ensure_ascii=False), 404
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True,"message": "伺服器內部錯誤"}, ensure_ascii=False), 500



#API根據景點編號取得景點資料-----------------------------------------------
@app.route("/api/attraction/<int:attractionID>", methods=["GET"])
def get_attraction(attractionID):
    try:
        # 連線資料庫
        con = mysql.connector.connect(  
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4"
        )
        cursor = con.cursor()
        
        if attractionID:
            # 執行SQL指令，去資料庫裏面查詢
            cursor.execute("SELECT id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions WHERE id = %s", (attractionID,))
            
            # 將查詢到的資料存放在taipeidaytrip的變數中
            taipeidaytrip_attractionid = cursor.fetchall()
        # 關閉游標和連線
        cursor.close()
        con.close()      

        if taipeidaytrip_attractionid:
            print(taipeidaytrip_attractionid)
            attractions = []
            for row in taipeidaytrip_attractionid: 
                # 將圖片URL轉換為Python列表
                images = json.loads(row[9])

                # 移除圖片URL中的反斜杠符號
                cleaned_images = [image.replace("\\", "") for image in images]

                attraction = {
                    "id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "description": row[3],
                    "address": row[4],
                    "transport": row[5],
                    "mrt": row[6],
                    "lat": float(row[7]),
                    "lng": float(row[8]),
                    "images": cleaned_images  # 使用處理後的圖片URL列表
                }
                attractions.append(attraction)

            response_data = {
                "data": attractions
            }
            return json.dumps(response_data, ensure_ascii=False), 200
        else:
            return json.dumps({"error": True,"message":"景點編號不正確"}, ensure_ascii=False), 404
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True,"message": "伺服器內部錯誤"}, ensure_ascii=False), 500


#API取得捷運站名稱列表--------------------------------------------------
@app.route("/api/mrts", methods=["GET"])
def apimrts():
    mrtslist_1 = []  # 初始化 mrtslist_1 變量
    try:
        # 連線資料庫
        con = mysql.connector.connect(  
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4"
        )
        cursor = con.cursor()
        
       
        # 執行SQL指令，去資料庫裏面查詢
        query_1 = "SELECT mrt FROM mrtslist WHERE mrt is not NULL ORDER BY attractionscount DESC"
        cursor.execute(query_1)
        
        # 將查詢到的資料存放在mrtslist_1的變數中
        mrtslist_1 = cursor.fetchall()
        print(mrtslist_1)
        # 關閉游標和連線
        cursor.close()
        con.close()

        if mrtslist_1:
            marts = []
            for row in mrtslist_1:  
                mrt = row[0]                    
                marts.append(mrt)

            response_data = {
                "data": marts
            }
            return json.dumps(response_data, ensure_ascii=False), 200
        else:
            return json.dumps({"error": True}, ensure_ascii=False), 404
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True,"message": "伺服器內部錯誤"}, ensure_ascii=False), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)