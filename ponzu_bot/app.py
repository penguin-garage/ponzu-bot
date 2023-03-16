from slack_bolt import App
from ponzu_bot.config import SLACK_BOT_TOKEN
from ponzu_bot.logger import logger
from ponzu_bot.chatter import generate_reply

app = App(token=SLACK_BOT_TOKEN)

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

@app.event("message")
def message_channel(body, say, logger):
    logger.info(body)
