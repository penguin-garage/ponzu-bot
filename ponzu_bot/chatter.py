import json
import requests
from ponzu_bot.config import DIFY_API_KEY, DIFY_API_URL
from ponzu_bot.logger import logger
from ponzu_bot.repository.conversations import get_conversation

def dify_chat(*, user_input: str, user_id: str, thread_id: str) -> dict:
    try:
        # メンションを削除
        if "<@" in user_input and ">" in user_input:
            user_input = user_input.split('>', 1)[1].strip()

        request_url = f"{DIFY_API_URL}/v1/chat-messages"

        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        }

        conversation = get_conversation(thread_id=thread_id)
        logger.info(f"conversation: {conversation}")
        conversation_id = conversation.conversation_id if conversation else ""

        data = {
            "inputs": {},
            "query": user_input,
            "response_mode": "streaming",
            "conversation_id": conversation_id,
            "user": user_id
        }

        response = requests.post(request_url, json=data, headers=headers, stream=True)
        response.raise_for_status()

        full_answer = ""
        conversation_id = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data = json.loads(decoded_line[6:])
                    if data["event"] == "agent_message":
                        full_answer += data["answer"]
                    elif data["event"] == "message_end":
                        conversation_id = data["conversation_id"]
        

        return {"answer": full_answer.strip(), "conversation_id": conversation_id}
    except requests.RequestException as e:
        logger.error(f"APIリクエストエラー: {e}")
        if hasattr(e.response, 'text'):
            logger.error(f"レスポンス内容: {e.response.status_code} {e.response.text}")
        return {"answer": "ごめんなさいぽん。うまくお返事できないぽん。エラーが発生してるぺん。", "conversation_id": ""}
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        return {"answer": "ごめんなさいぽん。うまくお返事できないぽん。エラーが発生してるぺん。", "conversation_id": ""}
