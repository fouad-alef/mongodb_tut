from beanie import Document
from pydantic import Field

class User(Document):
    name: str = Field(...)
    age: int = Field(...)
