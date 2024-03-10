import pymysql
import pymysql.cursors
import pymysql.err
import json

import requests

import os

from dotenv import load_dotenv

load_dotenv()
# MariaDB 연결 설정
conn = pymysql.connect(
    host= os.getenv('DBHOST'),
    port=int(os.getenv('DBPORT')),
    user=os.getenv('DBUSER'),
    password=os.getenv('DBPASSWORD'),
    database=os.getenv('DATABASE'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)



# 쿼리 실행
with conn.cursor() as cursor:
    sql = "SELECT name, date, company, description, imageurl, tag, screenshots, autokwd, platform FROM v_gameData ORDER BY id ASC"
    cursor.execute(sql)
    rows = cursor.fetchall()

# JSON 형식으로 변환


result = json.dumps(rows, ensure_ascii=False)
#print(result)

result = json.loads(result)



for i in range(len(result)):
    screenshot_list = result[i]['screenshots'].split(', ')
    platform_list = result[i]['platform'].split(', ')
    autokwd_list = result[i]['autokwd'].split(', ')
    result[i]["screenshots"] = screenshot_list
    result[i]['platform'] = platform_list
    result[i]['autokwd'] = autokwd_list
    
    result[i]['path'] = 'games'
    result[i]['gindie'] = 'game'
    result[i]['yearmonth'] = result[i]['date'][:-3]
    result[i]['gameurl'] = ''
    result[i]['yturl'] = ''
    result[i]['adult'] = False
    
    
    
# JSON 형식 출력

print(json.dumps(result[0], ensure_ascii=False))
print(len(result))

cursor.close()


## POST TEST

url = os.getenv("APILOCAL_POST")
headers = {"Content-Type": "Application/json"}

data = json.dumps(result[0])
print(data)
response = requests.post(url = url, data = data, headers=headers)

print(response)
