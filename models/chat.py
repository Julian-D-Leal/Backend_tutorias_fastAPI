from typing import Optional
from pydantic import BaseModel

class Message(BaseModel):
    id: Optional[str]
    message: str
    sender: str
    receiver: str
    date: Optional[str]
    time: Optional[str]