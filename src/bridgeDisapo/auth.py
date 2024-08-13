from datetime import timedelta
from typing import Any
from fastapi import Depends, HTTPException, HttpException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from bridgeDisapo import crud, models, schemas
from bridgeDisapo.database import get_db

oauth_sheme = OAuth2PasswordBearer(tokenUrl="token")

class Settings(BaseModel):
    auth_secret_key: str = "eW91IGNhbnQgaGFjayBteSBzZWNyZXQgY29kZSBOZXZlcg=="

    authjwt_access_token_expires: timedelta = timedelta(days=365)


@AuthJWT.load_config
def get_config():
    return Settings()

def authenticate_user(
        db: Session,
        form_data: OAuth2PasswordRequestForm
) -> Any:
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credential"
        )
    return user

def create_access_token(
    user: models.User,
    Authorize: AuthJWT
) -> Any:
    return Authorize.create_access_token(
        subject=user.email,
        user_claims = {"role" : user.role.value}
    )


def get_current_user(
        Auhtorize: AuthJWT=Depends(),
        db: Session=Depends(get_db)
    ) -> Any:

    try:
        Auhtorize.jwt_required()
        username = Auhtorize.get_jwt_subject()
        user = crud.get_user_by_email(db, username)

        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credential")

def role_required(role: schemas.Role):
    def wrapper(current_user: models.User = Depends(get_current_user))-> Any:

        if current_user.role!= role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this resource")
        return current_user
    return wrapper







