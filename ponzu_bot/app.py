from slack_bolt import App
from ponzu_bot.config import SLACK_BOT_TOKEN
from ponzu_bot.logger import logger
from ponzu_bot.chatter import Chatbot

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def command_handler(body, say):
    """
    Handle mention events in the Slack chat
    """
    text = body['event']['text']
    user_id = body['event']['user']
    thread_ts = body['event']['ts']

    logger.info(f"Received message from {user_id}: {text}")

    reply = Chatbot(user_id=user_id).chat(text)
    logger.info(f"Generated reply: {reply}")

    say({
        "thread_ts": thread_ts,
        "text": f"{reply}"
    })

@app.event("message")
def message_channel(body, say, logger):
    logger.info(body)
