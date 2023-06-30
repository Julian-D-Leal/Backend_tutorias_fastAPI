from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Calification(BaseModel):
    id_tutor: str = Field(..., alias="id_tutor")
    calif: float = Field(..., alias="calif")

class Clicks(BaseModel):
    asignatura_id: str
    tutor_id: str

class User(BaseModel):
    id: Optional[str]
    name: str
    career: str
    avaliability: list[list[int]]
    format: Optional[str]
    format_tutor: Optional[str]
    is_tutor: bool = Field(default=False)
    cost_tutor: Optional[int]
    type_tutor: Optional[str]
    password: str
    email: EmailStr
    budget: Optional[float]#presupuesto
    method: Optional[list[str]]
    method_tutor: Optional[list[str]]
    type_group: Optional[str]
    type_group_tutor: Optional[str]
    subjects_tutor: Optional[list[str]]
    keywords: Optional[list[str]]
    calification: Optional[list[Calification]]
    clicks: Optional[list[Clicks]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Juan",
                "career": "Ingeniería de Sistemas",
                "avaliability": [[1,0],[1,0,1,1]],
                "format": "Presencial",
                "format_tutor": "Presencial",
                "is_tutor": False,
                "cost_tutor": 0,
                "type_tutor": "Estudiante",
                "password": "12345678",
                "email": "juan@gmail.com",
                "budget": 25000,
                "method": ["",""],
                "method_tutor": ["",""],
                "type_group": "Grupal",
                "type_group_tutor": "Grupal",
                "subjects_tutor": ["id_Calculo","id_Programación"],
                "keywords": ["",""],
                "calification": [{"id_tutor": "12345","calif": 3.7}, {"id_tutor": "43254", "calif": 4.5}],
                "clicks": [{"asignatura_id": "id_Calculo","tutor_id": "12345"}, {"asignatura_id": "id_Programación", "tutor_id": "43254"}]
            }
        }

class LoginUserSchema(BaseModel):
    email: EmailStr
    #password: constr(min_length=8)
    password: str
    




