#for storing authentication and anything with jwt tokens

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# this will be end point from our login, so plug the routing name of our "LOGIN" route.. which is /login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY 
# Algorithm
# Expiration time of token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# literally to craete the secret access token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # copy of a dictionary

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# function to verify the access token (pass in token, and  )
def verify_access_token(token: str, credentials_exception):
    try:
        # store payload data 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # to extract the data... to user_id -- exact location where user.id is located
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        # this validates that it matches our specific token schema
        
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
        # token data is just what we called ID
    return token_data


# can pass as a dependency in any of our path operations.
#  WIll take token from request auto, extract id, verify token is correct by calling verify_access_token, 
# and extract id, and auto fetch user from db and ad it as parameter to path operation function

#* THIS IS IMPORTANT because WHERE YOU QUERY your DATABASE to grab the user, then you return the user. 
#* then Whatever you return in here, is ULTIMATELY what allows any of your other CRUD routes to RECEIVE what info you are returning. 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
   # call the function above to verify its a correct token
    # return verify_access_token(token, credentials_exception)

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user




#* LESGO!!!! COmposite key vs primary key
# Primary key - a SINGULAR column in your table that ensures that every single entry is unique.
# composite key - a primary key but one that spans over multiple columns 
# so composite(primary) doesnt care if there are duplicates per column, 
# HOWEVER: it checks if both columns have same data in TWO different rows.
# SO::: composite(primary) key UNIQUELY IDENTIFIES ROWS --, by cycling through the columns |
