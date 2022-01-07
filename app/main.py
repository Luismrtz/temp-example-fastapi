from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from .routers import post, user, auth, vote

#todo :Base Alch setup 
#! models related  : #todo :Base Alch setup
# from sqlalchemy.orm import Session
# from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from . import models, schema, utils #IMPORT SCHEMA file and IMPORT models file
from .database import engine
from .config import settings


#todo :Base Alch setup

# models.Base.metadata.create_all(bind=engine) #! CREATES ALL OF OUR MODELS via SQLALCHEMY | CAN COMMENT OUT ONCE HAVE ALEMBIC package INSTALLED

#Todo FAST API has built in documentation/swagger ui? on routes
#! 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
# WORK in Virtual Environment ----> source venv/Scripts/activate
# to start in development  ---> uvicorn  main:app --reload
# # now ---> uvicorn app.main:app --reload  (look inisde the app directory and find MAIN )    
# for production --> uvicorn  main:app
#* postgress requires psycopg  | mySQL requires MySQLdb to communicate to database
#* when using SQLAlchemy, we need to install the SQL's drivers to help communicate to database,
#*  in this case we already have psycopg2(1 type of SQL DRIVER) to communicate to database
#* SQLAlchemy generates SQL statements and psycopg2 sends SQL statements to the database. 
#* SQLAlchemy depends on psycopg2 or other database drivers to communicate with the database!

app = FastAPI()

origins = ["https://www.google.com"]
#? middleware: is a function that runs before every request
#? so when someone sends a request for our app, it will go to the middleware first and do its thang before it goes to the routers below
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#todo : BASE psycopg SETUP!!! NEEDED WHEN NOT USING SQLALCH~~~ also shouldnt expose this 
#todo: BUT NO NEED FOR THIS ANYMORE.. we are using SQLALCHEMY to connect to DATABASE now
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='root', password='root', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # create CUrose so can EXECUTE within each route/CRUD operation.
#         print("Database connection was successfull!!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)



#! router core ... when we get an http request, instead we go donw our list and all "router" routes within all other files specified below.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)