from beanie import Document
from pydantic import Field

class User(Document):
    name: str = Field(...)
    age: int = Field(...)




class Context(Document):
    context_id: str = Field(default_factory=lambda: str(uuid4()))
    school_id: str
    grade: int
    subject: str
    language: Language
    timestamp: str = Field(default_factory=current_timestamp)


class User(Document):
    message: str
    source: Source
    token_length: int
    timestamp: datetime


class Suggestions(Document):
    title: str
    prompt: str
    confidence: Optional[float]
    response_time: Optional[int]


class Bot(User):
    confidence: float
    suggestions: Optional[Suggestions]
    response_time: Optional[int]


class Session(Document):
    language: Language
    token_length: int
    feedback: bool


# ########################### Entities ############################


class UserContext(Document):
    user_id: str
    role: Role
    context: List[Context] = []
    timestamp: str = Field(default_factory=current_timestamp)


class ChatSession(Document):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    context_id: str
    course_id: Optional[str]
    activity_id: Optional[str]
    outcome_id: Optional[str]


class ChatCoversation(Document):
    user_id: str
    session_id: str
    remaining_token: int
    session_status: SessionStatus
    session_length: int
    session: List[Optional[Session]]
    timestamp: datetime