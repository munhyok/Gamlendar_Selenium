from core.database.Database import Database


db = Database('./upcoming/xbox/backup/2024-03-04 18:45:46_backup.csv')

def main():
    
    db.insert()
    
main()