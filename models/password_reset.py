from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PasswordReset(BaseModel):
    id: Optional[str]
    email: str
    token: Optional[str] = None
    expires: Optional[datetime] = None

class ChangePassword(BaseModel):
    token: str
    password: str
