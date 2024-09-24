import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from ponzu_bot.logger import logger

# 環境変数の確認
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
if not SERVICE_ACCOUNT_FILE:
    logger.error("環境変数 SERVICE_ACCOUNT_FILE が設定されていません。")
    raise EnvironmentError("環境変数 SERVICE_ACCOUNT_FILE が設定されていません。")

# 認証範囲を指定 (必要なスコープに応じて変更してください)
SCOPES = [
    'https://www.googleapis.com/auth/datastore',
    'https://www.googleapis.com/auth/dialogflow',
]

try:
    # サービスアカウントの認証情報を作成
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # アクセストークンを自動リフレッシュして取得
    credentials.refresh(Request())

    # アクセストークンを表示
    logger.info(f"Access Token: {credentials.token}")

    # トークンの有効期限を確認
    logger.info(f"Token Expiry: {credentials.expiry}")

    # 認証情報を返す
    def get_credentials():
        return credentials

except Exception as e:
    logger.error(f"認証エラー: {e}")
    raise