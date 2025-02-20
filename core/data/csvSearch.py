import pandas as pd
from core.database.Database import Database

def csvSearch(game_title):
    db = Database()
    
    timestamp = db.getTimestamp()
    
    platforms = [
        'steam',
        'playstation',
        'xbox',
        #'switch'
    ]
    
    for platform in platforms:
        df = pd.read_csv(f'./upcoming/{platform}/backup/{timestamp}.csv')
        try:
            contains = df[df['autokwd'].str.contains(fr'(^|,\s*){game_title}($|,\s*)', case=False, na=False, regex=True)]
            if not contains.empty:
                raw_list = contains['autokwd'].to_list()
                raw = raw_list[0].split(',')
                return raw[0]
            else:
                print(f"{platform}에 {game_title}이름이 없음")
        except:
            print(f"{platform}에 {game_title}이름이 없음")

    # 모든 플랫폼에서 검색에 실패하면 None 반환
    return None