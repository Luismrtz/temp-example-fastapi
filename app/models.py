
#todo :Base Alch setup (THE MODELS/SCHEME will look like)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean # to create a column | AND need to import TYPE



#! every model represents a table in our database. 
#! | WILL CREATE A TABLE
class Post(Base):  #The BASE model from SQLALCHEMY, we just have to extend it
    #What do we whant to name this TABLE in postgress? 
    __tablename__ = 'posts' # lets just call it posts
    #define the columns (starting point )
    id = Column(Integer, primary_key=True, nullable=False) # need to specify the datatype + other types based on SQL format
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False) #? to have database server send the DEFAULT. "server_default"
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #import TIMESTAMP & text.  
    #import text allows us to plug text/func? into our server's default values, that ISNT false/true based. 

#todo sql is not good with database migrations or making changes to it
#todo to autmatically make changes with SQL, need another software?? wait.. what was I referring to?.. ohhh: alembic
#todo datatype should match up with what the foreign key is. ForeignKey(__tablename__.id, parent is deleted then children will too  
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE" ), nullable=False)


    #!setting up a relationship, does NOTHING in database, 
    #! but it TELLS SQLALCHEMY to auto fetch some information based on relationship
    #return the ACTUAL sqlalchemy CLASSname of the other mode.  NOT the __tablename__ this time
    # this auto creates another property for our posts, so when we are retreiving a Post, 
    # it will return a owner property and figures out the relationship to User
    # so it will actually FETCH the USER based on the OWNER's ID and return it for us
    #? BUT MUST UPDATE SCHEMA FOR THIS TOO
    owner = relationship("User") 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True) #they have to provide an email + unique so email cant register twice
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #important to have a record of everything thats created in db, will come in handy
    

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    