from pydantic import BaseModel, Field, EmailStr
from typing import List
from typing import Optional

class Clicks(BaseModel):
    id_tutor: str

class Schedule(BaseModel):
    day: int
    hour: int

class Opinion(BaseModel):
    opinion: Optional[str]
    calification_tutor: float = Field(..., ge=0.5, le=5)
    name_user: str
    url_img: str


class User(BaseModel):
    name: str
    career: Optional[str]
    semester: Optional[int]
    availability: Optional[List[Schedule]]
    format: Optional[List[str]]
    format_tutor: Optional[List[str]]
    is_tutor: bool = Field(...,)
    is_student: bool = Field(...)
    cost_tutor: Optional[int] 
    type_tutor: Optional[str]
    password: str
    email: EmailStr
    budget: Optional[int]
    method: Optional[List[str]]
    method_tutor: Optional[List[str]]
    type_group: Optional[List[str]]
    type_group_tutor: Optional[List[str]]
    tutor_opinions: Optional[List[Opinion]]
    subjects_tutor: Optional[List[str]]
    keywords: Optional[List[str]]
    clicks: Optional[List[Clicks]]
    image_url: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Juan",
                "career": "Ingeniería de Sistemas",
                "semester": 5,
                "availability": [{"day":2,"hour": 5},{"day":1,"hour": 2}],
                "format": ["Presencial","Virtual"],
                "format_tutor": ["Virtual"],
                "is_tutor": False,
                "is_student": True,
                "cost_tutor": 0,
                "type_tutor": "Estudiante",
                "password": "12345678",
                "email": "juan@gmail.com",
                "budget": 25000,
                "method": ["",""],
                "method_tutor": ["",""],
                "type_group": ["Grupal"],
                "tutor_opinions": [{"opinion": "Muy buen tutor", "calification": 4.5}, {"opinion": "Buen tutor", "calification": 3.5}],
                "type_group_tutor": ["Grupal","Individual"],
                "subjects_tutor": ["id_Calculo","id_Programación","etc"],
                "keywords": ["",""],
                "calification": [{"id_tutor": "12345","calif": 3.7}, {"id_tutor": "43254", "calif": 4.5}],
                "clicks": [{"asignatura_id": "id_Calculo","tutor_id": "12345"}, {"asignatura_id": "id_Programación", "tutor_id": "43254"}],
                "image_url": "http://azure.blob.com/12345.jpg"
            }
        }

class LoginUserSchema(BaseModel):
    email: EmailStr
    #password: constr(min_length=8)
    password: str

class FileBase(BaseModel):
    dataUrl: str
    format: str