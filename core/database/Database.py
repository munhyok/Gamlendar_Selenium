import pymysql.cursors
import pymysql.err
import mariadb
import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd
import time


#   Workflow
#   CSV파일을 MariaDB로 옮기기
#   옮긴 MariaDB를 JSON 형태로 변환
#   변환 후 MongoDB로 이동
#   
#   SQL의 COUNT를 사용해 기존에 있는 테이블의 ROW를 수집하고
#
#   Commit후의 테이블 ROW 수집
#   그 다음 업로드

#   concatData 부분에서 Database 인스턴스를 생성하는 부분과
#   main.py 부분의 Database 인스턴스 생성을 각각 하다보니 서로 값 공유가 되지 않는다.
#   Database 클래스는 하나의 인스턴스만 생성해 사용해야한다.
#   간단한 싱글톤 패턴으로 구현해보자

COUNT_TABLE_ROW = """SELECT COUNT(*) FROM gamlendarDB.v_gameData"""

class Database:
    load_dotenv()
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        
        return cls._instance
    
    def __init__(self):
        
        if not self._initialized:
            self.url = os.getenv("APILOCAL_POST")
            try:
                self.connection = pymysql.connect(
                    host= os.getenv('DBHOST'),
                    port=int(os.getenv('DBPORT')),
                    user=os.getenv('DBUSER'),
                    password=os.getenv('DBPASSWORD'),
                    database=os.getenv('DATABASE'),
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
            except pymysql.MySQLError as e:
                print(f"Error connecting to MariaDB: {e}")

            self.before_count = self.tableCount()
            self.after_count = 0

            print(f"{self.before_count} 현재 DB 게임 수")
            
            #중복 init 방지
            self._initialized = True
        


    def tableCount(self):

        with self.connection.cursor() as cursor:
            cursor.execute(COUNT_TABLE_ROW)
            rowNumber = cursor.fetchone()
            rowCount = rowNumber["COUNT(*)"]
            
        return rowCount
        
    
    def __insert(self, csv):
        
        filterList = ['Adult Game', 'Old Steam Page']

        
        self.df = pd.read_csv(csv, encoding='utf-8', header=0)
        
        df = self.df
        
        sql_game = """INSERT INTO game_table (title, release_date, company, description, thumbnail_image, tag) values(%s,%s,%s,%s,%s,%s)"""
        sql_screenshot = """INSERT INTO screenshot_table (title, image) values(%s, %s)"""
        sql_autokwd = """INSERT INTO autokwd_table (title, autokwd) values(%s, %s)"""
        sql_platform = """INSERT INTO platform_table(title, platform) values(%s, %s)"""
        
        
        with self.connection.cursor() as cursor:
            
            
            for index, row in df.iterrows():
                
                if row['description'] not in filterList: 
                    autokwds = row['autokwd'].split(',')
                    screenshots = row['screenshot'].split(',')
                    platforms = row['platform'].split(',')

                    print(autokwds)

                    try:
                        cursor.execute(sql_game,(row['title'], row['date'], row['company'], row['description'], row['imageurl'], row['tag']))
                    except pymysql.err.IntegrityError as e:
                        print(e)

                    try:
                        for autokwd in autokwds:
                            cursor.execute(sql_autokwd, (row['title'], autokwd))
                    except pymysql.err.IntegrityError as e:
                        print(e)

                    for screenshot in screenshots:
                        cursor.execute(sql_screenshot, (row['title'], screenshot))


                    for platform in platforms:
                        cursor.execute(sql_platform, (row['title'], platform))
               

            try:
                response = requests.get(url= self.url+"/gamlendar")
                response.raise_for_status()

                self.connection.commit()
                print('Commit Complete')
                
                
                
                
            except requests.exceptions.RequestException as e:
                print("에러 발생 FastAPI 확인 필요: ", e)
                self.connection.rollback()

            except pymysql.ProgrammingError as e:
                print("cursor 에러발생: ", e)
                self.connection.rollback()
        
        
        
        
        
    
    
    def __migrateMongo(self):
        
        
        self.after_count = self.tableCount()
        index = self.after_count - self.before_count

        print(f"업로드할 게임 수 {index}")
        print("10초 뒤에 데이터 이동")
        time.sleep(10)

        with self.connection.cursor() as cursor:

            new_game_sql = """SELECT name, date, company, description, imageurl, tag, screenshots, autokwd, platform FROM gamlendarDB.v_gameData ORDER BY id DESC LIMIT """ + str(index)
            cursor.execute(new_game_sql)
            new_data = cursor.fetchall()

            result_raw = json.dumps(new_data, ensure_ascii=False)
            result = json.loads(result_raw)


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
  
        print(f"{index}개 게임 업로드 완료")
        return result
        
        
        
        
    def __postMongo(self, raw_json):
        
        headers = {"Content-Type": "Application/json"}

        
        
        for i in range(len(raw_json)):
            data = json.dumps(raw_json[i])
            
            response = requests.post(url = self.url, data = data, headers=headers)

            print(response)
            
     
            
    def findGame(self, name):
        name = f"%{name}%"
        sql_findGame = """SELECT name FROM gamlendarDB.v_gameData WHERE autokwd LIKE %s"""
        
        
        
        with self.connection.cursor() as cursor:
            
            cursor.execute(sql_findGame, name)
            sql_fetch = cursor.fetchone()
            
            print(sql_fetch)
            if sql_fetch == None:
                return None
            
            result = sql_fetch['name']
        
        return result
        
    
    
    def migrateMongo(self):
        games = self.__migrateMongo()
        self.__postMongo(games)
    
    def insert(self, csv):
        self.__insert(csv)
        
        

