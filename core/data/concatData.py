import pandas as pd
import time
from datetime import datetime

from core.database.Database import Database




def concat_data(gameList, detailList, date, platform):
    
    db = Database()
     
    timestamp = db.getTimestamp()
     
    gameList_df = pd.DataFrame(gameList)
    detailList_df = pd.DataFrame(detailList)
    
    concatResult = pd.concat([gameList_df, detailList_df], axis=1, join='inner')
    
    
    for i in range(len(concatResult)):
        
        concatResult['title'][i] = concatResult['autokwd'][i].split(',')[0]
    
    concatResult.to_csv('./upcoming/'+platform+'/backup/'+timestamp+'.csv', index=False)
    
    
    #db.insert('./upcoming/'+platform+'/backup/'+date+'_backup'+ '.csv')
    
    return concatResult