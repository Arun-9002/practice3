
from sqlalchemy import Column,Integer,String
from backend.database import Base


class Register(Base):
    __tablename__ = 'register' 
    id = Column(Integer, primary_key=True,index=True)
    name=Column(String(50))
    email=Column(String(50))
    phone=Column(String(50))
    password=Column(String(50))


class Login(Base):
    __tablename__ = 'login'

    email = Column(String(50), primary_key=True)
    password = Column(String(50))
       
    