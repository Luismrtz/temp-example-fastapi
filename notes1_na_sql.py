from typing import Optional
from fastapi import FastAPI, Response ,status, HTTPException
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
#* SQLAlchemy is an ORM - Object-relational mapping 
#* when using SQLAlchemy, we need to install the SQL's drivers to help communicate to database,
#*  in this case we already have psycopg2(1 type of SQL DRIVER) to communicate to database
#* SQLAlchemy generates SQL statements and psycopg2 sends SQL statements to the database. 
#* SQLAlchemy depends on psycopg2 or other database drivers to communicate with the database!

#! 204 is delete *note* when you send back a 204, you dont want to be sending any data back ... AT LEAST for fastAPI
# ? instead you should return a RESPONSE(status_code=status.HTTP_204_NO_CONTENT)
#! 200 is successful
#! 201 is post
#! 404 is ...

app = FastAPI()



#defines the schema for the POST request, and will spit out an error if not a str or null
#! BASICALLY the BaseModel is the Schema  {describes the name of each item and its type}
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # default value
    # IMPORT optional from TYPING.  
    # rating: Optional[int] = None # to make this schema optional (none by default)


#* pyscopg
while True:
    try:
        # conn = psycopg2.connect(host='localhost', database='fastapi', user='root', password='root', cursor_factory=RealDictCursor)
        conn = psycopg2.connect(host='localhost', database='<databaseName>', user='<user>', password='<password>', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        # if we want to wait a few seconds before it re-runs the while loop if failed to connect
        time.sleep(2)


#? note: lists are ARRAYS in Python,  Dicts are just object collections with datavalues
#? NOTE +:  dicts/objects are "hashed structures of key and value pairs" but NO ORDER is maintained within a dict, except by ID's 
#! A DICTIONARY(the whole collection/ data structure/ associative array) ----
#! ----is basicaly an object array{holds key: value pairs}, but we can invoke it with a shortcut .dict() with python 
#? dictionarys are muttable, but KEYS are NOT.   values are tho...   {"Key1": "value1"}
#? you cannot sequence a dictionary by INDEX, but only by KEYS/ID's
my_posts = [{"title": "title of post 1", "content": "content of post", "published": True, "id": 1},
            {"title": "title of post 2", "content": "abcdefg", "published": False, "id":2}
]

def find_post(id):
    for p in my_posts: 
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts): #iterate over array, and grab specific index using enumerate (p is each POST in array/ i is INDEX)
        if p['id'] == id:  
            print(i) # literal index
            return i  #gives index of dictionary / returns literal index number 

# this decorator turns the function into a path operation (an end point to hit when using our api)
@app.get('/') # root path /
def root():
    return{"message": "welcome to my api"}

@app.get("/posts") # assigning the path /posts to retrieve posts,
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts} # fastAPI automatically cerializes this array into JSON format so we can send it to our api






#* this doesnt matter, just for notes
@app.post("/NOTEScreateposts", status_code=status.HTTP_201_CREATED)
def NOTES_create_posts(post: Post):
    post_dict = post.dict() 
    post_dict['id'] = randrange(0, 1000000000) # auto plug an ID to the created Schema with RAND number 
# def create_posts(payload: dict = Body(...)):
    #payload: can be named anything
    # payload: dict = Body(...) 
    # --is how to extract all fields from body, and convert to python dictonary, then save inside the variable payload
    print(Post) #* pydantic model just looks like this, title='string'... .... no brackets
    #* to convert pydantic model to a dictionary {'title': 'string'....}
    # print(Post.dict())

    my_posts.append(post_dict) #append - put that object to END of "my_posts" object array
    return {"data": post_dict}

#? ORDER matters....THIS NEEDS to be above {ID} 
#? because route is SIMILAR and FASTapi has no way of knowing which ROUTE is WHICH if they are SUPER SIMILAR
@app.get("/posts/latest")
def get_lastest_post():
    post = my_posts[len(my_posts) -1] # last object entry in array
    return {"detail": post}




#* THIS ARE JUST NOTES
@app.get('/NOTES_posts/{id}')
    # ?type is a string, need to convert to int| FASTapi can validate the "ID" to be an int within the POST function
def NOTES_get_post(id: int, response: Response): #fast api auto extracts ID and can place into this function
    print(id)  
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND   #! to force it to change the status code
        # return {'message': f"post with id: {id} was not found"}
        # ? PROPER way to catch an error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}




@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index in array that has required ID
    # my_post.pop(index) to remove from array
    index = find_index_post(id) # insert id, get that index number as int
    if index == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id) # insert id, get that index number as int
    if index == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    post_dict = post.dict() # take data we got from front-end/insomnia in this case ( structured by Post schema) && converts to a dictionary()
    post_dict['id'] = id  #match that (front-end/insomnia)Post's ID with ROUTE:ID
    my_posts[index] = post_dict # we mutate/update our (front-end/insomnia) object data with that specific data value
    return {'data': post_dict}
