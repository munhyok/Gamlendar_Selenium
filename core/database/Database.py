import pymysql.cursors
import pymysql.err
import mariadb
import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd


class Database:
    load_dotenv()
    
    def __init__(self):

        
        try:
            self.connection = pymysql.connect(
                host= os.getenv('DBHOST'),
                port=int(os.getenv('DBPORT')),
                user=os.getenv('DBUSER'),
                password=os.getenv('DBPASSWORD'),
                database=os.getenv('DATABASE'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            
        self.curr = self.connection.cursor()
    
    def __insert__(self, csv):
        
        self.df = pd.read_csv(csv, encoding='utf-8', header=0)
        
        df = self.df
        
        sql_game = """INSERT INTO game_table (title, release_date, company, description, thumbnail_image, tag) values(%s,%s,%s,%s,%s,%s)"""
        sql_screenshot = """INSERT INTO screenshot_table (title, image) values(%s, %s)"""
        sql_autokwd = """INSERT INTO autokwd_table (title, autokwd) values(%s, %s)"""
        sql_platform = """INSERT INTO platform_table(title, platform) values(%s, %s)"""
        
        
        with self.curr as cursor:
            for index, row in df.iterrows():
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
               
        self.connection.commit()
        print('OK')
        
        cursor.close()
        
        
        
    
    
    
        
    def __saveIndex__(self,index, filename):
        with open(filename, 'r+') as file:
            data = json.load(file)
            data["index"] = index

        
        json_file = open(filename, 'w', encoding='utf-8')
        json.dump(data, json_file)
        json_file.close()
            
        
    def __loadIndex__(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return data["index"]
    
    
    def __migrateMongo__(self):
        
        self.index = self.__loadIndex__('./core/database/db_index.json')
        

        
        cursor = self.connection.cursor()
        
        sql = f"SELECT name, date, company, description, imageurl, tag, screenshots, autokwd, platform FROM v_gameData ORDER BY id ASC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()

        
        

        result_raw = json.dumps(rows, ensure_ascii=False)
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


        
        #games = json.dumps(result, ensure_ascii=False)
        
        
        self.__saveIndex__(len(result), './core/database/db_index.json')

        
        
        return result
        
        
        
        
    def __postMongo__(self, result):
        index = self.index
        url = os.getenv("APILOCAL_POST")
        headers = {"Content-Type": "Application/json"}

        
        
        for i in range(index, len(result)): # ex) index = 51 len(result) = 58
            data = json.dumps(result[i])
            #print(data)
            response = requests.post(url = url, data = data, headers=headers)

            print(response)
    
    
    def migrateMongo(self):
        games = self.__migrateMongo__()
        self.__postMongo__(games)
    
    def insert(self, csv):
        self.__insert__(csv)
        
        self.migrateMongo()
        #self.connection.close()
        
        
