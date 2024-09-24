from pydantic import BaseModel

class Conversation(BaseModel):
    conversation_id: str
    thread_id: str
    user_id: str