from typing import Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    id: Optional[str]
    message: str
    sender: str
    receiver: str
    date: Optional[str]
    time: Optional[str]
    read: bool | None = Field(default=False)