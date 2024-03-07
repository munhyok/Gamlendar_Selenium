import pymysql.cursors
import pymysql.err
import mariadb
import os
from dotenv import load_dotenv
import pandas as pd


class Database:
    load_dotenv()
    
    def __init__(self, csv):
        
        
        
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
        self.df = pd.read_csv(csv, encoding='utf-8', header=0)
    
    def __insert__(self):
        
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
        self.connection.close()
    
    def insert(self):
        self.__insert__()
        #self.connection.close()
        
        
