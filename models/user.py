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
    avaliability: list[list[int]] = [[1,0],[1,0,1,1]]
    format: Optional[str]
    format_tutor: Optional[str]
    is_tutor: bool = Field(default=False)
    cost_tutor: Optional[int]
    type_tutor: Optional[str]
    password: str
    email: EmailStr
    budget: Optional[float]#presupuesto
    method: Optional[list[str]] = ["",""]
    method_tutor: Optional[list[str]] = ["",""]
    type_group: Optional[str]
    type_group_tutor: Optional[str]
    subjects_tutor: Optional[list[str]] = ["Calculo","Programación"]
    keywords: Optional[list[str]] = ["",""]
    calification: Optional[list[Calification]] = [{"id_tutor": "","calif": 0.0}, {"id_tutor": "", "calif": 0.0}]
    clicks: Optional[list[Clicks]] = [{"asignatura_id": "","tutor_id": ""}, {"asignatura_id": "", "tutor_id": ""}]






