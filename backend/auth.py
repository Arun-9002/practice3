from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from .database import get_db
from .models import Register
from .schemas import UserCreate, UserRead, UserLogin

app = FastAPI()

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/register", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if len(payload.phone) != 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    new_user = Register(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password=payload.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/register", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(Register).all()


@app.delete("/register/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == payload.email).first()

    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@app.post("/refresh")
def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        new_access = create_access_token({"sub": payload["sub"]})
        return {"access_token": new_access}
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
