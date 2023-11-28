# 수집 실패 로그입니다. Exception Handling 할 때 활용합니다.

FAILEDLIST = []

def failed_log(collect, title, log, platform):
    
    if collect == True:
        FAILEDLIST.append([title,log,platform])
        
    else: return FAILEDLIST