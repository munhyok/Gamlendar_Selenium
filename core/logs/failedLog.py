# 수집 실패 로그입니다. Exception Handling 할 때 활용합니다.
# logging 사용해서 로그 수집
import logging

failedLogs = {
    'pc': [],
    'xbox': [],
    'playstation': [],
    'switch': []
}


def failed_log(collect, title, log, platform):
    
    
    if collect == True:
        failedLogs[platform].append([title,log])
        
    else:
        tmp = failedLogs[platform]
        return tmp
    