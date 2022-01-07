from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint
#todo our SCHEMA/PYDANTIC/type interface:: defines the structure of a REQUEST &&& RESPONSE!!!!
#!! schema defines our request and response. ok ok cool
#!! so works like a type interface, but solely exclusive to REQUESTS/RESPONSE CRUD
#!! NEEDED TO SECURE WHAT SHOULD/SHOULDNT BE PASSED/RECEIVED BY USER
#!! helps with security and testing
# class PostTypes(BaseModel):
#     title: str
#     content: str
#     published: bool = True 
#* MODELS are different, they define how the FULL(column of) TABLE LOOKS LIKE in our DATABASE???

# creating different MODELS is nice because we can limit what fields the user can pass in depending on the type of CRUD operation
# ex. we could make updating a post be only limited to changing the TITLE 



#!!! USERSSSS

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime
    class Config: 
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# define a schema for the access token and token type
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

#! VOTE
class Vote(BaseModel):
    post_id: int
    # dir: conint(ge=0, le=1)
    voted: bool





#! POSTSSS
#* another way tho... is to just extend a class with different operations.
#* Making use of INHERITANCE


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True



class PostCreate(PostBase): #this is how you extend a class
    pass #just means it accepts everything , so esentially exactly the same as PostBase class



class PostResponse(PostBase):
    #? title, content, and published are included due to inheritance
    id: int
    created_at:datetime  #an easier way to define a DATE as a type in python
    owner_id: int
    owner: UserOut

    #NEED this to tell PYDANTIC model to read the data even if its not a dict.. 
    # if not it will throw an error. Because pydantic model will only read it if its a dictionary
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
