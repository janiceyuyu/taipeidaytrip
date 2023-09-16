import re
import json
import mysql.connector

def filter_image_urls(file_text):
    valid_formats = ['jpg', 'png']
    urls = re.findall(r'https:\/\/.*?(?:jpg|png)', file_text, re.IGNORECASE)
    filtered_urls = [url for url in urls if any(url.lower().endswith(format) for format in valid_formats)]
    return filtered_urls

# 讀取 JSON 檔案
with open('data/taipei-attractions.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 建立資料庫連線
con = mysql.connector.connect(
    user="root",
    password="12345678",
    host="localhost",
    database="taipeidaytrip"
)

cursor = con.cursor()

# 遍歷 JSON 資料並寫入資料庫
for entry in data['result']['results']:
    images = filter_image_urls(entry['file'])

    sql = "INSERT INTO attractions (id, rate, transport, name, date, lng, REF_WP, avBegin, langinfo, mrt, SERIAL_NO, RowNumber, category, MEMO_TIME, POI, images, idpt, lat, description, avEnd, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        entry['_id'],
        entry['rate'],
        entry['direction'],
        entry['name'],
        entry['date'],
        entry['longitude'],
        entry['REF_WP'],
        entry['avBegin'],
        entry['langinfo'],
        entry['MRT'],
        entry['SERIAL_NO'],
        entry['RowNumber'],
        entry['CAT'],
        entry['MEMO_TIME'],
        entry['POI'],
        json.dumps(images),  # 插入 JSON 格式的圖片 URL
        entry['idpt'],
        entry['latitude'],
        entry['description'],
        entry['avEnd'],
        entry['address']
    )
    cursor.execute(sql, values)

# 提交資料庫變更
con.commit()

# 關閉游標和資料庫連線
cursor.close()
con.close()