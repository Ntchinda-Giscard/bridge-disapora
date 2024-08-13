from typing import Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from bridgeDisapo import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str)-> Any:

    user = db.query(models.User).filter(models.User.email == email)

    return user

def create_user(db: Session, user: schemas.UserCreate) -> Any:

    hashed_pwd = pwd_context.hash(user.password)
    db_user = models.User(
        email = user.email,
        password = hashed_pwd,
        firstname = user.firtnmae,
        lastname = user.lastname,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except:
        db.rollback()
    finally:
        db.close()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user

