from fastapi import FastAPI, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from bridgeDisapo.database import engine, get_db
from app import models
from pydantic import BaseModel
from app.crud import create_user
from app.schema import UserCreate


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"response" : "hello baba"}

@app.post("/add_user")
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)