Generic single-database configuration.

To build a complete RBAC system with OAuth2 JWT token authentication, integrating everything into a database, and organizing the project with a proper file structure, you can follow these steps. We'll use SQLite for simplicity, but this can be easily replaced with any other database like PostgreSQL or MySQL.

### **1. Project Structure**

Let's start with the recommended project structure:

```
rbac_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── auth.py
│   └── dependencies.py
│
├── migrations/
│   └── (auto-generated Alembic migrations)
│
├── .env
├── requirements.txt
├── alembic.ini
└── README.md
```

### **2. Setup Dependencies**

In the `requirements.txt`:

```text
fastapi
uvicorn[standard]
sqlalchemy
pydantic
passlib[bcrypt]
fastapi-jwt-auth
python-dotenv
alembic
```

### **3. Database Setup**

#### `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### **4. Define Models**

#### `app/models.py`

```python
from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class Role(enum.Enum):
    CLIENT = "client"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role), default=Role.CLIENT)
```

### **5. Create Schemas**

#### `app/schemas.py`

```python
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role

class User(BaseModel):
    id: int
    username: str
    role: Role

    class Config:
        orm_mode = True
```

### **6. CRUD Operations**

#### `app/crud.py`

```python
from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=

from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

Let’s continue from where we left off. We were at the point of testing the system after setting everything up.

### **1. Complete Project Structure Recap**

Here’s how the project structure should look:

```
rbac_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── auth.py
│   └── dependencies.py
│
├── migrations/
│   └── (auto-generated Alembic migrations)
│
├── .env
├── requirements.txt
├── alembic.ini
└── README.md
```

### **2. Final Steps: Running and Testing the Application**

#### **1. Initialize the Database:**

Before you can run the application, you need to create the database schema. Here’s how to do it using Alembic:

1. **Run Alembic Migrations:**
   If you haven't already, initialize Alembic and generate the first migration:

   ```bash
   alembic init migrations
   ```

2. **Edit `alembic.ini`:**
   Set the `sqlalchemy.url` in `alembic.ini` to match your `DATABASE_URL`:

   ```ini
   sqlalchemy.url = sqlite:///./test.db
   ```

3. **Generate Migration:**
   After making sure the `env.py` in the `migrations/` folder is set up correctly, you can generate a migration:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

4. **Apply Migration:**
   Apply the migration to create the tables:

   ```bash
   alembic upgrade head
   ```

#### **2. Running the Application:**

Run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

#### **3. Testing the System:**

1. **Create Users:**
   Use a tool like Postman, Insomnia, or even `curl` to create users. Here's an example using `curl`:

   ```bash
   curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{
       "username": "client_user",
       "password": "client_password",
       "role": "client"
   }'
   ```

   Create an admin user similarly:

   ```bash
   curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{
       "username": "admin_user",
       "password": "admin_password",
       "role": "admin"
   }'
   ```

2. **Obtain JWT Tokens:**
   Authenticate and retrieve a JWT token:

   ```bash
   curl -X POST "http://127.0.0.1:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=client_user&password=client_password"
   ```

   This will return a JSON object with an `access_token` you can use to authenticate requests.

3. **Access Protected Routes:**
   Use the token to access routes protected by role-based access control:

   ```bash
   curl -X GET "http://127.0.0.1:8000/client/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

   Similarly, you can access admin routes:

   ```bash
   curl -X GET "http://127.0.0.1:8000/admin/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

### **3. Summary**

With this setup, you have a fully functional RBAC system with JWT-based authentication and OAuth2 password flow. The system can be expanded with more roles, more complex permission checks, or integrated with a different database.

If you want to further enhance this, consider adding:

- **Refresh Tokens:** To allow users to refresh their tokens without re-authenticating.
- **Role Hierarchy:** For more complex role-based access control.
- **Front-End Integration:** If you plan to build a front-end for your application.

This setup provides a strong foundation for securing your FastAPI application with role-based access control.