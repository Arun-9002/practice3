from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
import os

from .database import engine, Base, get_db
from .models import Register
from .schemas import UserCreate, UserRead, UserLogin

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# ACCESS TOKEN
def create_access_token(data: dict, expires_minutes: int = 30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# DECODE TOKEN
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None


# REFRESH TOKEN
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# REGISTER
@app.post("/register", response_model=UserRead)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if len(payload.phone) != 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    user = Register(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password=payload.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# GET USERS
@app.get("/register", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(Register).all()


# DELETE USER
@app.delete("/register/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# LOGIN
@app.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == payload.email).first()

    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})

    return {
        "user": user,
        "access_token": access,
        "refresh_token": refresh
    }


# REFRESH TOKEN
@app.post("/refresh")
def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": payload["sub"]})

    return {"access_token": new_access_token}
