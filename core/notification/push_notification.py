import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

load_dotenv()

def initializeFirebase():
    cred = credentials.Certificate('./core/notification/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    
    print('파이어베이스 인증완료')
    
def notification_message():
    message = messaging.Message(
        topic=os.getenv('FIREBASE_TOPIC'),
        notification=messaging.Notification(
            title='게임 정보 업데이트 완료!',
            body='겜린더에 새로운 게임 정보가 업데이트 되었어요!\n어떤 게임이 들어왔는지 확인해보세요!'
        ),
        
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                channel_id="500"
            )
        )
    )
    
    return message


def send_message():
    
    initializeFirebase()
    message = notification_message()
    
    
    try:
        response = messaging.send(message, dry_run=False)
        print(f"메시지 전송 완료")
    except:
        print(f"푸시 알림 전송 실패 다시 시도해주세요")