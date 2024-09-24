import os
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ponzu_bot.config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from ponzu_bot.logger import logger
from ponzu_bot.chatter import dify_chat
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from ponzu_bot.model import Conversation
from ponzu_bot.repository.conversations import save_conversation

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def command_handler(body, say):
    """
    Handle mention events in the Slack chat
    """
    text = body.get('event', {}).get('text') or ""
    user_id = body.get('event', {}).get('user')
    thread_ts = body.get('event', {}).get('thread_ts') or body.get('event', {}).get('ts')

    logger.info(f"Received message from {user_id}: {text}")

    reply = dify_chat(user_input=text, user_id=user_id, thread_id=thread_ts)
    output = reply["answer"]

    logger.info(f"Generated reply: {reply}")

    response = say({
        "thread_ts": thread_ts,
        "text": f"{output}"
    })

    logger.info(f"Response: {response}")
    thread_id = response.get("message", {}).get("thread_ts")
    conversation_id = reply["conversation_id"]

    if conversation_id:
        conversation = Conversation(conversation_id=conversation_id, thread_id=thread_id, user_id=user_id)
        save_conversation(conversation)
    


@app.message("hello")
def message_hello(message, say):
    # スレッドの開始または継続のためのタイムスタンプを取得
    thread_ts = message.get("thread_ts", message["ts"])

    # イベントがトリガーされたチャンネルへメッセージを送信します
    say(
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "プロジェクト更新"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "プロジェクトXの最新レポートです。"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*締め切り:*\n2024年8月15日"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*ステータス:*\n順調"
                    }
                ]
            },
            {
                "type": "image",
                "image_url": "https://cdn-ak.f.st-hatena.com/images/fotolife/e/eiki_okuma/20180525/20180525121815.jpg",
                "alt_text": "プロジェクトのイメージ"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "レポートを見る"
                        },
                        "action_id": "view_report"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "承認"
                        },
                        "style": "primary",
                        "action_id": "approve"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "却下"
                        },
                        "style": "danger",
                        "action_id": "deny"
                    }
                ]
            }
        ],
        text="プロジェクトXの最新レポートです。",
        thread_ts=thread_ts  # スレッドに返信するためのパラメータ
    )

# ボタンがクリックされたときのアクションを処理します
@app.action("view_report")
def action_view_report(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> がレポートを見ました。", thread_ts=body['message']['ts'])

@app.action("approve")
def action_approve(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> がプロジェクトを承認しました。", thread_ts=body['message']['ts'])

@app.action("deny")
def action_deny(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> がプロジェクトを却下しました。", thread_ts=body['message']['ts'])


@app.event("message")
def message_channel(body, say, logger):
    logger.info(body)


@app.middleware
def skip_retry(logger, request, next):
    if "x-slack-retry-num" not in request.headers:
        next()

class RestartHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            logger.info(f"変更を検出しました: {event.src_path}")
            os.execv(sys.executable, ['python'] + sys.argv)

def run_app():
    handler = RestartHandler()
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()

    try:
        logger.info("アプリケーションを起動しています...")
        SocketModeHandler(app, SLACK_APP_TOKEN).start()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    run_app()

if __name__ == "__main__":
    main()