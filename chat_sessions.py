import asyncio
import enum
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4

from beanie import Document, init_beanie
from beanie.operators import Set
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

connection_string = f"""mongodb://root:password@localhost:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true"""

@dataclass(init=False)
class Config:
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://root:password@localhost:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true",
    )
    DATABASE_NAME = "chatbot"
    COL_CHAT_CONTEXT = "chat_context"


def current_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


class SessionStatus(enum.Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class ChatSession(Document):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    context_id: str
    session_status: SessionStatus = Field(default=SessionStatus.STARTED)
    course_id: Optional[str]
    activity_id: Optional[str]
    outcome_id: Optional[str]
    timestamp: datetime


async def initialize():
    client = AsyncIOMotorClient(Config.MONGO_URI, username="root", password="password")
    await init_beanie(
        database=client[Config.DATABASE_NAME],
        document_models=[ChatSession],
    )


class ChatSessionManager:
    @staticmethod
    async def create_chat_session(user_id: str, context_id: str, course_id: Optional[str], 
                                  activity_id: Optional[str], outcome_id: Optional[str]):
        chat_session = ChatSession(
            user_id=user_id,
            context_id=context_id,
            course_id=course_id,
            activity_id=activity_id,
            outcome_id=outcome_id,
            session_status=SessionStatus.STARTED,
            session_length=0,
            timestamp=current_timestamp()
        )
        try:
            result = await ChatSession.insert_one(chat_session)
            logging.info(f"New chat session created with session_id : {chat_session.session_id}")
            return chat_session
        except PyMongoError as e:
            logging.error(f"Error creating chat session: {e}")
            return None

    @staticmethod
    async def end_chat_session(session: ChatSession) -> ChatSession:
        session.session_status = SessionStatus.FINISHED
        session.session_length = (datetime.utcnow() - session.timestamp).seconds
        try:
            await session.update(Set({ChatSession.session_status: session.session_status,
                                      ChatSession.session_length: session.session_length}))
            logging.info("Chat session ended with session_id : {}".format(session.session_id))
            return session
        except PyMongoError as e:
            logging.error("Error ending chat session: {}".format(str(e)))
            return None

    @staticmethod
    async def get_chat_session(session_id: str) -> Optional[ChatSession]:
        try:
            session = await ChatSession.find_one(ChatSession.session_id == session_id)
            if session:
                return session
            else:
                logging.warning(f"No chat session found with session_id : {session_id}")
                return None
        except PyMongoError as e:
            logging.error(f"Error retrieving chat session: {e}")
            return None


async def main():
    await initialize()
    # Create a new chat session
    new_session = await ChatSessionManager.create_chat_session(
        user_id=str(uuid4()),
        context_id=str(uuid4()),
        course_id="Math101",
        activity_id="HW1",
        outcome_id="Math1"
    )
    print(new_session)
    # End an existing chat session
    # updated_session = await ChatSessionManager.end_chat_session(session)

    # Retrieve a chat session by its session_id
    # session = await ChatSessionManager.get_chat_session("abcd1234")

asyncio.run(main())
