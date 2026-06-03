from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, init_db
from app import crud
from app.db import db_models

app = FastAPI(title="SanchayKosh API")

@app.on_event("startup")
def startup_event():
    """Create database tables when the app starts."""
    init_db()

def open_db():
    """Open a new database session for each request and ensure it is closed after the request is processed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to SanchayKosh API!"}

@app.post("/users/")
def create_new_user(username: str, db: Session = Depends(open_db)):
    """Endpoint to create a new user."""
    existing_user = crud.get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = crud.create_user(db, username)
    return {"message": f"User '{new_user.username}' created successfully", "user_id": new_user.id}