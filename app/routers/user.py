from fastapi import FastAPI, Response ,status, HTTPException, Depends, APIRouter # Depends is #todo Depends is a :Base Alch setup
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db  # models related| called from .database.py file



#! USE ROUTERS to IMPORT @app efficiently
router = APIRouter(
    prefix='/users',
    tags=["Users"]
)



# bad practice to call this create user for route path
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)# create is always 201
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password and store in a variable
    hashed_password = utils.hash(user.password)
    # we set the user.password to become the hashed_password | thus updating the pydantic user model
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() # to search based on id and grab the first one that comes up
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user