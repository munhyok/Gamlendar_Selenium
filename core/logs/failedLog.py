# 수집 실패 로그입니다. Exception Handling 할 때 활용합니다.

failedList = []

def failed_log(collect, title, log, platform):
    global failedList
    
    if collect == True:
        failedList.append([title,log,platform])
        
    else:
        tmp = failedList
        failedList = []
        return tmp
    