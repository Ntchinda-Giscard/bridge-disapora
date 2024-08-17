from typing import Any
from fastapi import Depends
from app.models import User
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schema import UserCreate


def create_user(user: UserCreate, db: Session = Depends(get_db)) -> Any:
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=user.password,
        role = user.role
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