from fastapi import FastAPI, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from bridgeDisapo.database import engine, get_db
from app import models
from pydantic import BaseModel
from app.models import User


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

@app.get("/")
async def read_root():
    return {"response" : "hello baba"}

@app.post("/add_user")
async def add_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=user.password
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)