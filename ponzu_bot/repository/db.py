from google.cloud import firestore
from ponzu_bot.auth import get_credentials

# Firestoreクライアントの初期化
def initialize_firestore():
    credentials = get_credentials() 
    firestore_client = firestore.Client(credentials=credentials)
    return firestore_client

# Firestoreクライアントの取得
db = initialize_firestore()

# データベース名を指定
from ponzu_bot.config import FIRESTORE_DATABASE_NAME
if FIRESTORE_DATABASE_NAME:
    db._database = FIRESTORE_DATABASE_NAME
