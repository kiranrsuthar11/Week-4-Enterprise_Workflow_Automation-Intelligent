from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterIn, TokenOut
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    username = data.username.strip()
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(409, "Username already exists")
    # The first registered account becomes admin; subsequent accounts are regular users.
    role = "admin" if db.query(User).count() == 0 else "user"
    user = User(username=username, password_hash=hash_password(data.password), role=role)
    db.add(user)
    db.commit()
    return {"message": "User registered", "role": role}

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not user.is_active or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Incorrect username or password")
    return {"access_token": create_access_token(user), "token_type": "bearer"}
