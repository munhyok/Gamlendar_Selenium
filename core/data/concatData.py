import pandas as pd
import time
from datetime import datetime




def concat_data(gameList, detailList, date, platform):
     
    gameList_df = pd.DataFrame(gameList)
    detailList_df = pd.DataFrame(detailList)

    concatResult = pd.concat([gameList_df, detailList_df], axis=1, join='inner')
    concatResult['title'] = concatResult['autokwd'].str[0]
    concatResult.to_csv('./upcoming/'+platform+'/backup/'+date+'_backup'+ '.csv', index=False)
    
    
    return concatResult