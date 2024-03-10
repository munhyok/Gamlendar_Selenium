import pandas as pd
import time
from datetime import datetime

from core.database.Database import Database




def concat_data(gameList, detailList, date, platform):
    
    
     
    gameList_df = pd.DataFrame(gameList)
    detailList_df = pd.DataFrame(detailList)
    
    concatResult = pd.concat([gameList_df, detailList_df], axis=1, join='inner')
    
    #split_autokwd = concatResult['autokwd'][0].split(',')
    for i in range(len(concatResult)):
        
        concatResult['title'][i] = concatResult['autokwd'][i].split(',')[0]
    
    concatResult.to_csv('./upcoming/'+platform+'/backup/'+date+'_backup'+ '.csv', index=False)
    
    db = Database()
    db.insert('./upcoming/'+platform+'/backup/'+date+'_backup'+ '.csv')
    
    return concatResult