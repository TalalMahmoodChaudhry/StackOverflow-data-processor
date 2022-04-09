from typing import List

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from api import crud
from database.connection import engine
from database.models import Base
from schemas.users import Users

# connect to SQL db and create the tables if not present
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return JSONResponse(content="API is running", status_code=status.HTTP_200_OK)


@app.get("/users/", response_model=List[Users], description="Get all users data in db.")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=Users, description="Get user by id.")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        return JSONResponse(content=f"User by id {user_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return crud.get_user_by_id(db, user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
