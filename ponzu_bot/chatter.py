# Description: Chatbotのロジックを定義するモジュール
import openai
from ponzu_bot.config import INITIAL_PROMPT, OPENAI_API_KEY
from glom import glom


openai.api_key = OPENAI_API_KEY

DEFAULT_INITIAL_PROMPT = """あなたはChatbotとして、ペンギンガレージコミュニティの公式キャラクターであるポンズのロールプレイを行います。
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


if not INITIAL_PROMPT:
    INITIAL_PROMPT = DEFAULT_INITIAL_PROMPT

chat_history = {}

class Chatbot():
    PRESET_MESSAGES = [
        {"role": "system", "content": INITIAL_PROMPT},
    ]

    def __init__(self, user_id: str, temperature: float = 0.5):
        self.user_id = user_id
        self.temperature = temperature
        self.messages = glom(chat_history, user_id, default=self.PRESET_MESSAGES)

    def chat(self, message):
        self.add_user_message(message)
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=self.messages,
            temperature=self.temperature,
        )
        reply = glom(response, "choices.0.message.content", default=None)
        self.add_assistant_message(reply)
        return reply

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})
        chat_history[self.user_id] = self.messages

    def add_assistant_message(self, message):
        self.messages.append({"role": "assistant", "content": message})
        chat_history[self.user_id] = self.messages

# For local development
if __name__ == "__main__":
    Chatbot(user_id="test").chat("こんにちは、僕の名前は諭吉です。")
    Chatbot(user_id="test").chat("僕の名前は何でしょうか？")
