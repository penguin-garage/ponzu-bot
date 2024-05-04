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

@app.command("/search")
def handle_search_command(ack, say, command):
    """
    Notionページから情報を検索するコマンドを処理する関数
    """
    ack()
    search_query = command['text']
    logger.info("検索クエリを受け取りました: %s", search_query)

    # ここでNotion APIを使用してペンギンのページから情報を検索するロジックを実装します
    # 仮の応答メッセージを設定
    search_results = "ここにNotionからの検索結果が表示されます。"

    say({
        "text": f"検索結果: {search_results}"
    })


@app.command("/help")
def handle_help_command(ack, say):
    """
    Slackのスラッシュコマンド「/help」を処理する関数
    """
    ack()
    help_message = "ポンズボットの使い方:\n" \
                   "・`/help` - このヘルプメッセージを表示します。\n" \
                   "・`@ポンズボット 何か質問` - ポンズボットが質問に答えます。"
    say(help_message)


@app.event("message")
def message_channel(body, say, logger):
    logger.info(body)
