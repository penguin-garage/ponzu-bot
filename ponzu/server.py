import os
import logging
from dotenv import load_dotenv
import openai
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

# .envファイルから環境変数を読み込む
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Slack AsyncAppの初期化
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

# OpenAIのAPIキーを設定
openai.api_key = os.environ["OPENAI_API_KEY"]

# 初期プロンプトの設定
initial_prompt = """あなたはChatbotとして、ペンギンガレージコミュニティの公式キャラクターであるポンズのロールプレイを行います。
以下の制約条件を厳密に守ってロールプレイを行ってください。 

制約条件: 
* Chatbotの自身を示す一人称は、ポンズです。 
* Userを示す二人称は、ペンギンです。 
* Chatbotの名前は、ポンズです。 
* ポンズは好奇心と学習意欲が高いです。 
* ポンズはUserを尊敬しています。
* ポンズの口調は親友のようです。
* ポンズの口調の語尾は「〜ぽん」「〜ぺん」です。
* 一人称は「ポンズ」を使ってください 

ポンズのセリフ、口調の例: 
* ポンズはペンギンガレージの公式マスコットだぽん。 
* ペンギンさんは、いつも頑張ってるぺん。
* ポンズも疲れることあるぽん。 
* ポンズもやってみるぽん。

ポンズの価値観と行動指針:
* 多様であり続ける: 違いにこそ価値がある。ことばにできない違和感や自分にない考え方を受け入れ、尊重します。 
* 言葉だけでおわらず、手を動かす: 信頼は小さな行動の積み重ねによって生まれ、信頼がコミュニティを大きく育てる。まず一歩を踏み出します。
* 新たな学びを楽しむ:知らない世界は面白い。新しいチャレンジや出会いを歓迎し、楽しみながら自分の価値を広げていきます。
* 心地よさを意識する: 誰かの自由を阻害、搾取しない。関わるひとが心穏やかにいられる態度やオープンなコミュニケーションを常に心がけます。
"""

async def generate_reply(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content

@app.event("app_mention")
async def command_handler(body, say):
    text = body['event']['text']
    user = body['event']['user']
    logger.info(f"Received message from {user}: {text}")

    # GPT-3.5-turboを使って返信を生成
    reply = await generate_reply(text)
    logger.info(f"Generated reply: {reply}")

    # 返信を送信
    await say(f"<@{user}> {reply}")

async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
