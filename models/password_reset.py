from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PasswordReset(BaseModel):
    email: str
    token: Optional[str] = None
    expires: Optional[datetime] = None

class ChangePassword(BaseModel):
    token: str
    password: str

class ChangePasswordAuth(BaseModel):
    actualPassword: str
    newPassword: str
