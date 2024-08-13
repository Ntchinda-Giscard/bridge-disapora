from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from bridgeDisapo.database import Base
import enum
from sqlalchemy import ForeignKey


class Role(enum.Enum):
    CLIENT = "client"
    ADMIN = "admin"
    STAFF = "staff"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True )
    firstname= Column(String, unique=False, nullable=True)
    lastname = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, unique=False, nullable=False)
    role = Column(Enum(Role), unique=False, nullable=False, default=Role.CLIENT.value)
    service_id = Column(Integer, ForeignKey("service.id"), nullable=True)
    service = relationship("Service", back_populates="user")


class Service(Base):

    __tablename__="service"

    id = Column(Integer, primary_key=True, index=True )
    name = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=True)
    users = relationship("User", back_populate="service")
