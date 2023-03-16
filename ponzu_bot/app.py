# Description: Slack BoltのAsyncAppを初期化する
from slack_bolt import App
from ponzu_bot.config import SLACK_BOT_TOKEN
from ponzu_bot.logger import logger
from ponzu_bot.chatter import generate_reply

# Slack AsyncAppの初期化
app = App(token=SLACK_BOT_TOKEN)

# app_mentionイベントを受け取る


@app.event("app_mention")
def command_handler(body, say):
    """
    Handle mention events in the Slack chat
    """
    text = body['event']['text']
    user = body['event']['user']
    logger.info(f"Received message from {user}: {text}")

    # GPT-3.5-turboを使って返信を生成
    reply = generate_reply(text)
    logger.info(f"Generated reply: {reply}")

    # 返信を送信
    say(f"<@{user}> {reply}")
