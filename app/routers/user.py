from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags = ['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_users(user:schemas.UserCreate,db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user