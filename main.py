from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from database import engine, get_db
from auth import hash_password, verify_password, create_access_token


# Create database tables
models.Base.metadata.create_all(bind=engine)


# Create FastAPI app
app = FastAPI(title="Professional Todo API")


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ROOT
@app.get("/")
def read_root():
    return {
        "message": "Hello, Intern!"
    }



@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }



# ==========================
# USER REGISTER
# ==========================

@app.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(models.User)
        .filter(
            (models.User.email == user.email) |
            (models.User.username == user.username)
        )
        .first()
    )


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )


    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user




# ==========================
# USER LOGIN
# ==========================
@app.post("/login", response_model=schemas.Token)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not db_user:
        print("User not found")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    print("Email :", user.email)
    print("Entered Password :", user.password)
    print("Stored Hash :", db_user.hashed_password)

    password_ok = verify_password(
        user.password,
        db_user.hashed_password
    )

    print("Password Match :", password_ok)

    if not password_ok:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }