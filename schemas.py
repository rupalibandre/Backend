from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# =====================
# USER SCHEMAS
# =====================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str



# =====================
# TODO SCHEMAS
# =====================

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "Medium"
    category: Optional[str] = "General"
    due_date: Optional[date] = None



class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[date] = None



class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    category: str
    due_date: Optional[date]
    user_id: int


    model_config = {
        "from_attributes": True
    }