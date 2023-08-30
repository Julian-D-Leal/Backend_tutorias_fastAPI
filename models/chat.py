from typing import Optional
from pydantic import BaseModel

class Message(BaseModel):
    id: Optional[str]
    message: str
    sender: str
    receiver: str
    date: Optional[str]
    time: Optional[str]
    
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "1",
                "message": "Hola, ¿cómo estás?",
                "sender": "1",
                "receiver": "2",
                "date": "2021-05-12",
                "time": "12:00"
            }
        }