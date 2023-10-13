from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector
import jwt
from datetime import datetime, timedelta
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")


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

#API註冊一個新的會員-----------------------------------------------
@app.route("/api/user", methods=["POST"])
def apiuser():
    signUpData = request.get_json()
    name=signUpData["name"]
    email = signUpData["email"]
    password = signUpData["password"]
    
 
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
        
        check_email = "SELECT email FROM member WHERE email = %s"
        cursor.execute(check_email, (email,))
        existing_email = cursor.fetchone()
        

        if existing_email:
            cursor.close()
            con.close()
            return json.dumps({"error": True, "message": "註冊失敗，重複的 Email"}, ensure_ascii=False), 404

        else:
            sql = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
            values = (name, email, password)
            cursor.execute(sql, values)
            con.commit()
            
           # 關閉游標和連線
            cursor.close()
            con.close()
        
            return json.dumps({"ok":True}, ensure_ascii=False), 200
            
        
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True, "message": "伺服器內部錯誤"}, ensure_ascii=False), 500

#API取得當前登入的會員資訊----------------------------------------------- 
@app.route("/api/user/auth")
def authorization():
    try:
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return "Authorization header is missing", 401

        parts = authorization_header.split()
        token = parts[1]

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        expiredTime = decoded_token["exp"]
        currentTime = int(datetime.utcnow().timestamp())

        user_id = decoded_token['id']
        email = decoded_token['email']
        name = decoded_token['name']

    except jwt.ExpiredSignatureError:
        return json.dumps({'error': True, 'message': '憑證已過期'}, ensure_ascii=False), 401
    except jwt.InvalidTokenError:
        return json.dumps({'error': True, 'message': '無效憑證'}, ensure_ascii=False), 401
    except Exception as e:
        return json.dumps({'error': True, 'message': '伺服器內部錯誤'}, ensure_ascii=False), 500

    try:
        # 連接資料庫
        con = mysql.connector.connect(
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4"
        )
        cursor = con.cursor()

        cursor.execute("SELECT id, email, name from member WHERE id = %s and email = %s and name = %s", (user_id, email, name))
        checkmember = cursor.fetchone()

        cursor.close()
        con.close()

        if checkmember and expiredTime > currentTime:
            return json.dumps({'id': user_id, 'name': name, 'email': email}, ensure_ascii=False), 200
        else:
            return json.dumps({'error': None, 'message': '信箱或密碼輸入錯誤'}, ensure_ascii=False), 404

    except mysql.connector.Error as err:
        return json.dumps({'error': True, 'message': '伺服器內部錯誤'}, ensure_ascii=False), 500







#API登入會員帳號-----------------------------------------------  
@app.route("/api/user/auth", methods = ["PUT"])
def signin():
    signInData = request.get_json()
    email = signInData["email"]
    password = signInData["password"]
    
    try:
        # 連接資料庫
        con = mysql.connector.connect(
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4"
        )
        cursor = con.cursor()

        # 執行SQL指令，查詢資料庫
        cursor.execute("SELECT id, email, password, name from member WHERE email = %s and password = %s", (email, password))
        # 將查詢到的資料放在checkmember
        checkmember = cursor.fetchone()
        print(checkmember)

        if checkmember:
            member_data = {
				"id": checkmember[0],
				"email": checkmember[1],
				"name": checkmember[3],
				 "exp": datetime.utcnow() + timedelta(days=7)
            }

            token = jwt.encode(member_data, SECRET_KEY, algorithm="HS256")
            response_success = json.dumps({'token': token}, ensure_ascii=False) # 檢查結果若確定OK，則提供token給前端
           
            
            # 關閉游標和連線
            cursor.close()
            con.close()
            
            return response_success, 200

        else:
            return json.dumps({'error': True, 'message': '信箱或密碼輸入錯誤'}, ensure_ascii=False), 404

    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({'error': True, 'message': '伺服器內部錯誤'}, ensure_ascii=False), 500

#API取得尚未確認下單的預定行程 ----------------------------------------
@app.route("/api/booking")
def bookingget():
    try:
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return "Authorization header is missing", 401

        parts = authorization_header.split()
        token = parts[1]
        bearer = parts[0]
    
        if bearer == "Bearer" and token:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            
            expiredTime = decoded_token["exp"]
            currentTime = int(datetime.utcnow().timestamp())

            id = decoded_token['id']
            email = decoded_token['email']
            name = decoded_token['name']

    except jwt.ExpiredSignatureError:
            return json.dumps({'error': True, 'message': '憑證已過期'}, ensure_ascii=False), 401
    except jwt.InvalidTokenError:
            return json.dumps({'error': True, 'message': '無效憑證'}, ensure_ascii=False), 401
    except Exception as e:
            return json.dumps({'error': True, 'message': '伺服器內部錯誤'}, ensure_ascii=False), 501



    try:
        # 連線資料庫
        con = mysql.connector.connect(  
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4",
            buffered=True
        )
        cursor = con.cursor()
        
       
        # 執行SQL指令，去資料庫裏面查詢
        sql_query = "SELECT member.id, member.name, member.email, member.date, member.time, member.price,attractions.id, attractions.name, attractions.address, attractions.images FROM member left JOIN attractions ON member.attractionID = attractions.id WHERE member.id = %s and member.email = %s and member.name = %s"
        cursor.execute(sql_query, (id, email, name))
        
        # 將查詢到的資料存放在bookingdata的變數中
        bookingdata = cursor.fetchone()  
        print(bookingdata)
        

        
        # 關閉游標和連線
        cursor.close()
        con.close()    

        if bookingdata and bookingdata[9]:
            images = json.loads(bookingdata[9])
            # print("images:", images)

            first_image = images[0]
             # print("第一張圖片:", first_image)

            booking={
                "date":bookingdata[3].strftime("%Y-%m-%d"),
                "time":bookingdata[4],
                "price":bookingdata[5]
            }
            attraction = {
                "attraction":{
                "id": bookingdata[6],
                "name": bookingdata[7],
                "address": bookingdata[8],
                "images": first_image  # 使用處理後的圖片URL列表
            }}

            if bookingdata and expiredTime > currentTime:
                response_data = {"data": {**attraction, **booking}}
            return json.dumps(response_data, ensure_ascii=False), 200 
        elif expiredTime < currentTime:
            return json.dumps({"error": True, "message": "未登入系統，拒絕存取"}, ensure_ascii=False), 403
        else:
            return json.dumps({"data": None}, ensure_ascii=False)
        
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return json.dumps({"error": True, "message": "伺服器內部錯誤"}, ensure_ascii=False), 500
    

#API建立新的預定行程 -------------------------------------------------
@app.route("/api/booking", methods = ["POST"])
def bookingpost():
    bookingpostdata=request.get_json()
    attractionID=bookingpostdata["attractionID"]
    date=bookingpostdata["date"]
    time=bookingpostdata["time"]
    price=bookingpostdata["price"]
    
    
    try:
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return "Authorization header is missing", 401

        parts = authorization_header.split()
        token = parts[1]

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        expiredTime = decoded_token["exp"]
        currentTime = int(datetime.utcnow().timestamp())

        id = decoded_token['id']
        email = decoded_token['email']
        name = decoded_token['name']

    except Exception as e:
            return json.dumps({'error': True, 'message': '未登入系統，拒絕存取'}, ensure_ascii=False), 403



    try:
        # 連線資料庫
        con = mysql.connector.connect(  
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4",
            buffered=True
        )
        cursor = con.cursor()
        cursor.execute("SELECT id, email, name, attractionID, date, time, price from member WHERE id = %s and email = %s and name = %s", (id, email, name))
        existing_user = cursor.fetchone()
        print(existing_user)

        if existing_user and expiredTime > currentTime:
            cursor.execute("UPDATE member SET attractionID = %s, date = %s, time = %s, price = %s WHERE id = %s", (attractionID, date, time, price, id))
			
            con.commit() #確定執行
            return json.dumps({"ok":True}, ensure_ascii=False), 200
        

        else:
            return json.dumps({"error": True, "message": "未登入系統，拒絕存取"}, ensure_ascii=False), 403
    except Exception as e:
            return json.dumps({'error': True, 'message': '伺服器內部錯誤'}, ensure_ascii=False), 500




#API刪除目前的預定行程 -----------------------------------------------   
@app.route("/api/booking", methods = ["DELETE"])
def bookingdelete():
    try:
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return "Authorization header is missing", 401

        parts = authorization_header.split()
        token = parts[1]

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        expiredTime = decoded_token["exp"]
        currentTime = int(datetime.utcnow().timestamp())

        id = decoded_token['id']
        email = decoded_token['email']
        name = decoded_token['name']

    except Exception as e:
            return json.dumps({'error': True, 'message': '未登入系統，拒絕存取'}, ensure_ascii=False), 403
    
    try:
        # 連線資料庫
        con = mysql.connector.connect(  
            user="root",
            password="12345678",
            host="localhost",
            database="taipeidaytrip",
            charset="utf8mb4",
            buffered=True
        )
        cursor = con.cursor()
        cursor.execute("SELECT id, email, name, attractionID, date, time, price from member WHERE id = %s and email = %s and name = %s", (id, email, name))
        existing_user = cursor.fetchone()
        print(existing_user)

        if existing_user and expiredTime > currentTime:
            cursor.execute("UPDATE member SET attractionID =NULL, date =NULL, time =NULL, price =NULL WHERE id = %s", (id,))
            con.commit() #確定執行
            return json.dumps({"ok":True}, ensure_ascii=False), 200
        

        else:
            return json.dumps({"error": True, "message": "未登入系統，拒絕存取"}, ensure_ascii=False), 403
    except Exception as e:
            return json.dumps({'error': True, 'message': '伺服器內部錯誤'}, ensure_ascii=False), 500





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)