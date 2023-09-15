from pydantic import BaseModel
from typing import Optional

#from bson import ObjectId

class Subject(BaseModel):
    name: str
    careers: list[str] = []
    semester: int


