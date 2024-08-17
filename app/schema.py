from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    CLIENT = "client"
    ADMIN="admin"
    STAFF="staff"

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    role: str