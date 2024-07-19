from core.database.Database import Database


def dataInsert():
    PLATFORM_LIST = [
        'steam',
        'playstation',
        'xbox',
        'switch'
    ]
    
    db = Database()
    
    timestamp = db.getTimestamp()
    

    for platform in PLATFORM_LIST:
        db.insert('./upcoming/'+platform+'/backup/'+{timestamp}+'.csv')
        
    