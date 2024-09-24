from google.cloud import firestore
from ponzu_bot.auth import get_credentials
from ponzu_bot.config import FIRESTORE_DATABASE_NAME

# Firestoreクライアントの初期化
def initialize_firestore():
    credentials = get_credentials()
    firestore_client = firestore.Client(credentials=credentials)
    if FIRESTORE_DATABASE_NAME:
        firestore_client._database = FIRESTORE_DATABASE_NAME
    return firestore_client

# Firestoreクライアントの取得
db = initialize_firestore()
