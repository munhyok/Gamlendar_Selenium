from core.database.Database import Database


def dataInsert():
    PLATFORM_LIST = [
        #'steam',
        #'playstation',
        #'xbox',
        'switch'
    ]
    
    db = Database()
    
    timestamp = db.getTimestamp()
    timestamp = str(1727503635)

    for platform in PLATFORM_LIST:
        db.insert('./upcoming/'+platform+'/backup/'+timestamp+'.csv')
    
    #db.insert('./upcoming/'+'playstation'+'/backup/'+timestamp+'.csv')
        
    