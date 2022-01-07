from typing import Optional
from fastapi import FastAPI, Response ,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#Todo FAST API has built in documentation/swagger ui? on routes
#! 1, 2, 3, 4, 5, 6, 
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






#todo type model use for NON-SQLALCH
class Post(BaseModel):
    title: str
    content: str
    published: bool = True 


#todo : BASE psycopg SETUP!!! NEEDED WITH + W/o0 SQLALCH~~~ also cant EXPOSE this info
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='<databaseName>', user='<user>', password='<password>', cursor_factory=RealDictCursor)
        # conn = psycopg2.connect(host='localhost', database='fastapi', user='root', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor() # create CUrose so can EXECUTE within each route/CRUD operation.
        print("Database connection was successfull!!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)



#!!!!!!! OUR QUERIESSSS:::  REGULAR SQL vs ORM(SQLalchemy|basic python methods|)

@app.get('/') # root path /
def root():
    return{"message": "welcome to my api"}


@app.get("/posts") # assigning the path /posts to retrieve posts,
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #!! NEVER DO THIS with sql: cursor.execute(f" INSERT INTO posts (title, content, puglished) VALUES ({post.title}, post.content...) ")
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # sanitizing/parametizing the values: MUST be this way so we are NOT vulnerable to SQL INJECTION attacks,
    # PEOPLE could TYPE SQL in the input field, and it can INVOKE a SQL command/attack if we are not SANITIZED PROPERLY.
    # %s are just variables/placeholders/parameters1
    #  (post.title... are the 2nd parameters with assigned names included) 
    # ASSIGN second PARAMETERS BY REQUIRED PUBLISH ORDER for TABLE database
    # also anytime we create something in the database, we want to RETURN the created results
    # RETURNING * does that

    #? cant just save post above in a new variable when grabbing (RETURNING *) returned results
    #? to save that into a new VARIABLE with SQL, we have to do "new_post = cursor.fetchone()"  this will get what we RETURNED from RETURNING *
    new_post = cursor.fetchone()
    #? ANYTHING BEFORE commit are STAGED CHANGES, 
    # MSUT have a COMMIT CHANGE call to save it in database.
    conn.commit() # this will push those changes out
    return {"data": new_post}



@app.get("/posts/{id}") #still need to validate the ID as a number,
def get_post(id: int): # convert it to an INT, so we dont get funky jakls;dfk;a inputs
    #! if I get a WEIRD issue, that EXTRA COMMA  after (str(id),) seems to fix it
    cursor.execute(""" SELECT * from posts WHERE id = %s""", (str(id),)) # then convert it to a string for SQL command
    #? note: MUST convert parameters to string in order to pass it to SQL string command
    post = cursor.fetchone()
    # print(post)
    if not post:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"post_details": post}



@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # anytime we modify the database, we SHOULD return the results
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None: #if delete_post wasnt found, throw error
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None: # updated_post wasnt found
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return {'data':updated_post}
