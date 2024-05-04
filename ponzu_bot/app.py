from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ponzu_bot.config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from ponzu_bot.logger import logger
from ponzu_bot.chatter import Chatbot
from ponzu_bot.qa import qa_bot

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

@app.command("/qa")
def handle_search_command(ack, say, command):
    """
    Notionページから情報を検索するコマンドを処理する関数
    """
    ack()
    search_query = command['text']
    logger.info("検索クエリを受け取りました: %s", search_query)

    # ここでNotion APIを使用してペンギンのページから情報を検索するロジックを実装します
    # 仮の応答メッセージを設定
    search_results = qa_bot(search_query)

    say({
        "text": search_results
    })


@app.command("/help")
def handle_help_command(ack, say):
    """
    Slackのスラッシュコマンド「/help」を処理する関数
    """
    ack()
    help_message = "ぽんずの使い方:\n" \
                   "`/help` - このヘルプメッセージを表示します。\n" \
                   "`/qa` - ぽんずがペンギンwikiページに基づいて質問に答えます。\n" \
                   "`@ponzu` - ぽんずと雑談ができます。"
    say(help_message)


@app.event("message")
def message_channel(body, say, logger):
    logger.info(body)

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()