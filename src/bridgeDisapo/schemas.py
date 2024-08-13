from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    CLIENT = "client"
    ADMIN="admin"
    STAFF="staff"

class UserCreate(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    role: Role

class User(BaseModel):
    id: int
    email: str
    role: Role
    firstname: str
    lastname: str

    class Config:
        orm_mode = True
