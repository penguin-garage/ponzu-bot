import os
from google.oauth2 import service_account
from ponzu_bot.logger import logger

# 環境変数の確認
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
if not SERVICE_ACCOUNT_FILE:
    logger.error("環境変数 SERVICE_ACCOUNT_FILE が設定されていません。")
    raise EnvironmentError("環境変数 SERVICE_ACCOUNT_FILE が設定されていません。")

# 認証範囲を指定 (必要なスコープに応じて変更してください)
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/datastore',
]

# サービスアカウントの認証情報を作成
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# 認証情報を返す
def get_credentials():
    return credentials