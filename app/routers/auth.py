from fastapi import FastAPI, Response ,status, HTTPException, Depends, APIRouter # Depends is #todo Depends is a :Base Alch setup
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schema, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):

    #{ "username": "asdflk",
    #   "password": ";alskdfja"}
    #? we trying to make it where we can plug user/passs in FORMDATA in insomnia
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # pass in the plain text password + the hashed password in db
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create a token
    #return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})


    return {"access_token": access_token, "token_type": "bearer"}