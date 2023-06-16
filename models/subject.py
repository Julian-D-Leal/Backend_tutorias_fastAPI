from pydantic import BaseModel
from typing import Optional

#from bson import ObjectId

class Subject(BaseModel):
    id: Optional[str]
    name: str
    careers: list[str] = []
    semester: int
