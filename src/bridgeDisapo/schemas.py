from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    CLIENT = "client"
    ADMIN="admin"
    STAFF="staff"

# class UserCreate(BaseModel):
#     # id: 
#     email: str
#     password: str
#     firstname: str
#     lastname: str
#     # role: Role

class User(BaseModel):
    # id: Optional[int]
    email: str
    password: str
    # role: Role
    firstname: str
    lastname: str

    class Config:
        orm_mode = True
