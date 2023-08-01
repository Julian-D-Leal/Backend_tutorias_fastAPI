from pydantic import BaseModel, Field, EmailStr
from typing import List
from typing import Optional

class Calification(BaseModel):
    id_tutor: str = Field(..., alias="id_tutor")
    calif: float = Field(..., alias="calif")

class Clicks(BaseModel):
    asignatura_id: str
    tutor_id: str

class Schedule(BaseModel):
    day: int
    hour: int

class User(BaseModel):
    id: Optional[str]
    name: str
    career: Optional[str]
    avaliability: Optional[List[Schedule]]
    format: Optional[List[str]]
    format_tutor: Optional[List[str]]
    is_tutor: bool = Field(default=False)
    cost_tutor: Optional[int]
    type_tutor: Optional[str]
    password: str
    email: EmailStr
    budget: Optional[float]#presupuesto
    method: Optional[List[str]]
    method_tutor: Optional[List[str]]
    type_group: Optional[List[str]]
    type_group_tutor: Optional[List[str]]
    subjects_tutor: Optional[List[str]]
    keywords: Optional[List[str]]
    calification: Optional[List[Calification]]
    clicks: Optional[List[Clicks]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Juan",
                "career": "Ingeniería de Sistemas",
                "avaliability": [{"day":2,"hour": 5},{"day":1,"hour": 2}],
                "format": ["Presencial","Virtual"],
                "format_tutor": ["Virtual"],
                "is_tutor": False,
                "cost_tutor": 0,
                "type_tutor": "Estudiante",
                "password": "12345678",
                "email": "juan@gmail.com",
                "budget": 25000,
                "method": ["",""],
                "method_tutor": ["",""],
                "type_group": ["Grupal"],
                "type_group_tutor": ["Grupal","Individual"],
                "subjects_tutor": ["id_Calculo","id_Programación","etc"],
                "keywords": ["",""],
                "calification": [{"id_tutor": "12345","calif": 3.7}, {"id_tutor": "43254", "calif": 4.5}],
                "clicks": [{"asignatura_id": "id_Calculo","tutor_id": "12345"}, {"asignatura_id": "id_Programación", "tutor_id": "43254"}]
            }
        }

class LoginUserSchema(BaseModel):
    email: EmailStr
    #password: constr(min_length=8)
    password: str
    