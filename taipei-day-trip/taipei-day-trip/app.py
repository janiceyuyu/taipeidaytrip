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
            # 使用 SQL 的 LIMIT 和 OFFSET 實現分頁
            query = "SELECT id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions WHERE mrt = %s OR name LIKE %s LIMIT %s OFFSET %s"
            keyword_pattern = f"%{keyword}%"
            cursor.execute(query, (keyword, keyword_pattern, per_page, page * per_page))
        else:
            # 如果未提供關鍵字，則檢索所有資料
            query = "SELECT id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions LIMIT %s OFFSET %s"
            cursor.execute(query, (per_page, page * per_page))
            
        # 將查詢到的資料存放在taipeidaytrip的變數中
        taipeidaytrip = cursor.fetchall()

        # 關閉游標和連線
        cursor.close()
        con.close()

        # 檢查是否還有更多的資料
        has_more = len(taipeidaytrip) == per_page

        if taipeidaytrip:
            attractions = []
            for row in taipeidaytrip:
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

            next_page = page + 1 if has_more else None

            response_data = {
                "nextPage": next_page,
                "data": attractions
            }
            return json.dumps(response_data, ensure_ascii=False), 200
        else:
            return json.dumps({"error": True}, ensure_ascii=False), 404
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True, "message": "伺服器內部錯誤"}, ensure_ascii=False), 500



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
            taipeidaytrip_attractionid = cursor.fetchone()  # 使用fetchone()获取一行数据而不是fetchall()

        # 關閉游標和連線
        cursor.close()
        con.close()      

        if taipeidaytrip_attractionid:
            print(taipeidaytrip_attractionid)

            # 將圖片URL轉換為Python列表
            images = json.loads(taipeidaytrip_attractionid[9])

            # 移除圖片URL中的反斜杠符號
            cleaned_images = [image.replace("\\", "") for image in images]

            
            attraction = {
                "id": taipeidaytrip_attractionid[0],
                "name": taipeidaytrip_attractionid[1],
                "category": taipeidaytrip_attractionid[2],
                "description": taipeidaytrip_attractionid[3],
                "address": taipeidaytrip_attractionid[4],
                "transport": taipeidaytrip_attractionid[5],
                "mrt": taipeidaytrip_attractionid[6],
                "lat": float(taipeidaytrip_attractionid[7]),
                "lng": float(taipeidaytrip_attractionid[8]),
                "images": cleaned_images  # 使用處理後的圖片URL列表
            }

            response_data = {
                "data": attraction  # 直接返回单个景点字典
            }
            return json.dumps(response_data, ensure_ascii=False), 200
        else:
            return json.dumps({"error": True, "message": "景點編號不正確"}, ensure_ascii=False), 404
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True, "message": "伺服器內部錯誤"}, ensure_ascii=False), 500


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