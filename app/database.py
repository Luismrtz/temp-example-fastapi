
#todo :Base Alch setup
#! FROM HERE: is basically a cut and paste >>
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#? when working with databases, there's a unique URL that you create to connect to any database, 
#? the format is...
#? NOTE: need this stuff in a secure file
#* SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address\hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://root:root@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#then what we have to do is create an engine! :responsible for sql alchemy to establish a connection to database
# when using a createENgine function, with SQL lite database, have to pass (SQLALCHEMY_DATABASE_URL,
# connect_args=('check_same_thread": false))
#this is esclusive to SQLlite : NOT NEEDED WITH POSTGRESS tho
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# AND to talk to a sql database, we need to do a SESSIOn
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #default values

#all of our models that we defined to create tables, will be extending the BASE class
#DEFINE base class
Base = declarative_base()

#todo MODEL/SQLALCHEMY RELATED: LAST THING TO DO is CREATE A DEPENDENCY (this is also provided in documents of SQLAlchemy)
# this session object is responsible for talking with the database,
# and so this created function will get the session from the DB, 
# and every time we get a request, we will get a session/ send sql to it,
# then when it is done, we close it out. 
#* now all CRUD calls with have a CUT/PASTE SESSION call linked to this function, 
#todo :Base Alch setup : KEEP ALL OF DATABASE INITIALIZATION CODE SEPARATELY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#! TO HERE: is basically a cut and paste <<