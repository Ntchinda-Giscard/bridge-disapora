from fastapi import FastAPI, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from bridgeDisapo import crud, models, schemas, auth
from bridgeDisapo.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = auth.authenticate_user(db, form_data)
    access_token = auth.create_access_token(user, Authorize)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/admin/", dependencies=[Depends(auth.role_required(schemas.Role.ADMIN))])
def admin_only_endpoint():
    return {"message": "Hello, Admin!"}

@app.get("/client/", dependencies=[Depends(auth.role_required(schemas.Role.CLIENT))])
def client_only_endpoint():
    return {"message": "Hello, Client!"}

