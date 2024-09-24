from google.cloud import firestore
from .db import db
from ponzu_bot.model import Conversation
from ponzu_bot.logger import logger

# 会話を保存する関数
def save_conversation(conversation: Conversation) -> None:
    try:
        doc_ref = db.collection('conversations').document(conversation.conversation_id)
        doc_ref.set(conversation.model_dump()) 
        logger.info(f"Conversation {conversation.conversation_id} with thread {conversation.thread_id} and user {conversation.user_id} saved successfully.")
    except Exception as e:
        logger.error(f"Error saving conversation: {e}")

# conversation_id, thread_id, user_idで該当のデータを取得する関数
def get_conversation(*, conversation_id: str = None, thread_id: str = None, user_id: str = None) -> Conversation:
    try:
        conversations_ref = db.collection('conversations')
        query = conversations_ref

        filters = {
            'thread_id': thread_id,
            'conversation_id': conversation_id,
            'user_id': user_id
        }

        for field, value in filters.items():
            if value:
                query = query.where(field, '==', value)

        results = query.stream()
        for doc in results:
            logger.info(f"Found conversation: {doc.to_dict()}")
            return Conversation(**doc.to_dict())
        logger.info("No matching conversation found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        return None
