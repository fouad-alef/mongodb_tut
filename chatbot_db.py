# from dotenv import find_dotenv, load_dotenv
import asyncio
import enum
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import uuid4

from beanie import Document, init_beanie
from beanie.operators import Set

# from domain.model import Context, UserContext
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

connection_string = f"""mongodb://root:password@localhost:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true"""


def current_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


class Language(enum.Enum):
    EN = "en"
    AR = "ar"


class Role(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"


class Context(Document):
    context_id: str = Field(default_factory=lambda: str(uuid4()))
    school_id: str
    grade: int
    subject: str
    language: Language
    timestamp: str = Field(default_factory=current_timestamp)


class UserContext(Document):
    user_id: str
    role: Role
    context: List[Context] = []
    timestamp: str = Field(default_factory=current_timestamp)


class Task(Document):
    content: str = Field(max_length=200)
    is_complete: bool = Field(default=False)


class User(BaseModel):
    user_id: str
    role: Role
    school_id: str
    grade: int
    subject: str
    language: Language


@dataclass(init=False)
class Config:
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://root:password@localhost:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true",
    )
    DATABASE_NAME = "chatbot"
    COL_CHAT_CONTEXT = "chat_context"


async def initialize():
    client = AsyncIOMotorClient(Config.MONGO_URI, username="root", password="password")
    await init_beanie(
        database=client[Config.DATABASE_NAME],
        document_models=[UserContext, Context],
    )


class UserRegistration:
    @staticmethod
    async def add_user(user: User):
        user_context = UserContext(
            user_id=user.user_id,
            role=user.role,
            context=[
                Context(
                    school_id=user.school_id,
                    grade=user.grade,
                    subject=user.subject,
                    language=user.language,
                )
            ],
        )
        result = await UserContext.insert_one(user_context)
        logging.info("New user added with user_id : {}".format(user.user_id))
        return result

    @staticmethod
    async def update_user(user_request: User, user: UserContext):
        user.context.append(
            Context(
                school_id=user_request.school_id,
                grade=user_request.grade,
                subject=user_request.subject,
                language=user_request.language,
            )
        )
        await user.update(Set({UserContext.context: user.context}))
        logging.info("Use with user_id : {} updated with new context".format(user_request.user_id))
        return user

    @staticmethod
    async def get_user(user, context):
        return await UserContext(
            user_id=user.user_id,
            role=user.role,
            context=[
                Context(
                    school_id=context.school_id,
                    grade=context.grade,
                    subject=context.subject,
                    language=context.language,
                )
            ],
        )

    @staticmethod
    async def user_exists(user: User):
        result = await UserContext.find_one(UserContext.user_id == user.user_id)
        return result

    @staticmethod
    async def context_exists(user_request: User, user):
        result = await user.find_one(
            UserContext.context.school_id == user_request.school_id,  # type: ignore [attr-defined]
            UserContext.context.grade == user_request.grade,  # type: ignore [attr-defined]
            UserContext.context.subject == user_request.subject,  # type: ignore [attr-defined]
            UserContext.context.language == user_request.language,  # type: ignore [attr-defined]
        )
        return result


    @staticmethod
    async def retrieve(user_request: User):
        user = await UserRegistration.user_exists(user_request)
        if user:
            context = await UserRegistration.context_exists(user_request, user)
            result = context if context else await UserRegistration.update_user(user_request, user)
        else:
            result = await UserRegistration.add_user(user_request)
        return result


async def main():
    await initialize()
    user = User(
        user_id=str(uuid4()),
        role=Role.STUDENT,
        school_id=str(uuid4()),
        grade=4,
        subject="math",
        language=Language.EN
    )
    # add the user to the database
    result = await UserRegistration.add_user(user)
    print(result)

    new_user = await UserRegistration.retrieve(user)
    print(new_user)


asyncio.run(main())