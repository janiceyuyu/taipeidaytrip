import json
import mysql.connector

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

# 創建一個字典來存儲每個 MRT 的景點名稱列表
mrt_attractions_dict = {}

# 遍歷 JSON 資料並處理 MRT 和相關的景點名稱
for entry in data['result']['results']:
    mrt = entry.get('MRT', '')  # 獲取 MRT，如果不存在則設為空字串
    name = entry.get('name', '')  # 獲取景點名稱，如果不存在則設為空字串

    # 將 MRT 加入字典並初始化景點名稱列表
    if mrt not in mrt_attractions_dict:
        mrt_attractions_dict[mrt] = []

    # 如果景點名稱存在並不在列表中，則添加到列表中
    if name and name not in mrt_attractions_dict[mrt]:
        mrt_attractions_dict[mrt].append(name)

# 遍歷 MRT 字典並將數據寫入 SQL
for mrt, attractions_list in mrt_attractions_dict.items():
    # 將景點名稱列表轉換為逗號分隔的字串
    attractions_str = ', '.join(attractions_list)
    # 計算景點數量
    attractions_count = len(attractions_list)

    # 構建 SQL 插入語句
    sql = "INSERT INTO mrtslist (mrt, attractions, attractionscount) VALUES (%s, %s, %s)"
    values = (mrt, attractions_str, attractions_count)

    cursor.execute(sql, values)

# 提交資料庫變更
con.commit()

# 關閉游標和資料庫連線
cursor.close()
con.close()