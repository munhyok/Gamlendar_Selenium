import datetime
import re

# 1985년 9월 13일
# 슈퍼 마리오 브라더스 출시일 - 그냥 내 인생 최초 게임이라 이스터애그 마냥 추가
# 발표 예정이나 출시 예정 게임은 1985년 9월 13일로 변환
# 

#분기는 과감하게 제거 그냥 연도 별로 구분할 예정

class DataCleaning:
    def __init__(self, platform):
        self._platform = platform
    
    
    
    def __date_clean(self, raw_data):
        
        if self._platform == 'steam':
            
            if raw_data == "발표 예정" or raw_data == "출시 예정 게임":
                return '1985-09-13'
            
            quarter_str = re.sub(r'\b[1-4]분기\b', '', raw_data)
            ymd_str = re.sub(r'[년월일]','',quarter_str)
            
            splitDate = ymd_str.split(' ')
            
            for i in range(len(splitDate)):
                splitDate[i] = splitDate[i].zfill(2)
                
            formatDate = '-'.join(splitDate)
            
            return formatDate
            
        elif self._platform == 'playstation':
            
            splitDate = raw_data.split('/')
            
            for i in range(len(splitDate)):
                splitDate[i] = splitDate[i].zfill(2)
                
            formatDate = '-'.join(splitDate)
            
            return formatDate
        
        elif self._platform == 'xbox':
            # xbox는 겜린더에 맞는 date형태로 되어있어 일단 보류..
            pass
        
        elif self._platform == 'switch':
            
            raw_data = raw_data[:-1]
            splitDate = raw_data.split('. ')
            
            for i in range(len(splitDate)):
                splitDate[i] = splitDate[i].zfill(2)
                
            formatDate = '-'.join(splitDate)
            
            return formatDate
        
        else: return None
        
    def formatDate(self, date):
        self.__date_clean(date)