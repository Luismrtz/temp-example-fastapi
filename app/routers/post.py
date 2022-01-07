# Depends is #todo Depends is a :Base Alch setup
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schema, oauth2
from sqlalchemy import func  # gives access to functions like SQL Count.
from ..database import get_db  # models related| called from .database.py file

#! USE ROUTERS to IMPORT @app efficiently
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#!!!!!!! OUR QUERIESSSS / ROUTESSSSSS:::  REGULAR SQL vs ORM(SQLalchemy|basic python methods|)
# to receive an array of our designed schema, we need to import LIST from typing
# @router.get("/", response_model=List[schema.PostResponse])
@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):  # todo :Base Alch setup + we call get_db from .database.py
    # same as cursor.execute( select * from posts  )
    # .all() RUNS the program in database and returns it( there's more like this, but this grabs ALL)
    # w/o that method call, it is nothing more than a sql command that hasnt been run

    # ? AUTHENTICATION: include .filter(models.Post.owner_id == current_user.id).all()  if LIMITING to only showing USER's POSTS.
    # ? AUTHENTICATION: KEEP as " db.query(models.Post).all " if allowing any user to see ALL POSTS

    # *set a default limit of 10 for "/posts?limit=..."  if no value was entered
   # *set a default skip of 0 and can now add a params number to skip.  "/posts?Limit=5&skip=1
   # *set a default SEARCH 0f "Optional[str] = "" " so it doesnt NEED a value by default. but once it receives one, we filter BASED on "models.Post.title.contains(search)"
    # * note, %20 == 'spacebar' when its in search params
   # THIS is how we will be setting up PAGINATION in the front-end


    #? for reference, prev version lol
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(
    #     limit).offset(skip).all()
          # pass in the specific model/schema for this query
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # ? DOING A JOIN here:
    # ?  But SQLAlchemy does an INNER join by default, (so we need to include OUTER if we want outer)
    # ? WHhile SQL(database) does an OUTER join by default (via sql query command)
    # this here is joining two tables and counting each post's total votes
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(
        limit).offset(skip).all()
    # print(posts)
    return posts

#! RESPONSE_MODEL=.... schema.PostResponse... is how we can limit what to return back to user from database


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
# testing code is a little easier by including the whole db: Session = ...
# ? user_id: int = Depends(oauth2.oauth2.get_current_user)  ... this function will now be a dependency, forces the user to be logged in before creating a post.
# ? so when this function is called, create_posts, frist thing we do is call that function "get_current_user" to verify auth
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # * TO DESTRUCT THE TYPES and AUTOPLUG/autoPASS to models.Post BASED on our typeINTERFACE and its REQURIED+DEFAULT-FIELDS... :D nice!
    # * **post.dict() will auto-unpack what we NEED for our models/SCHEMA.Post
    # new_post =  models.Post(title=post.title, content=post.content, published=post.published)

    # todo to pass in the owner's ID for the REQUIRED field (owner's id for post schema),
    # todo we grab the ID by who is currently logged in/authentication status. via "current_user.id"
    # todo and SPREAD it into models.Post()
    # print(current_user.id)
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # SQLALCHEMY's WAY OF ADDING TO DATABASE
    db.add(new_post)
    # SQLALCHEMY's WAY OF COMMITTING TO DATABASE
    db.commit()
    # SQLALCHEMY's WAY OF RETURNING/retreiving THE COMMITED DATA
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int,  db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    # * looks for the post in database with the id based on if it matches what the user has requested.
    # use .first() when dealtihng with finding ONLY ONE . INSTEAD of ATTACHING .all(waste of resouces)
    # one_post = db.query(models.Post).filter(models.Post.id == id).first()



    one_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    # ? :D (:  We going with a FaceBook/ SOCIAL MEDIA style tho, so we'd like people to able to see posts.
    # ? AUTHENTICATION:RAISE: include "IF one_post.owner_id != current_user.id: "  if LIMITING to only showing USER's specific POSTS.
    # if one_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # no need toADD or commit or refresh() because we aren't mutating.
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return one_post


@router.delete("/{id}")
# haha remember, DONT need to CONVERT id:int to STRING and %s to sanitze code for SQL queries with ALCHEMY
def delete_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)

    post_delete = delete_query.first()

# to check if there is a post with that
    if post_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    # if we did find the query we want to delete (query_delte)
    # and these two HAVE TO MATCH (checking if user is OWNER of post)
     # ? (variable)current_user = oath2.get_current_user
    if post_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # ? if no "RAISE" then we grab original query and append a delete.
    # look it up, this is just how you delete and update the change in query for sqlalchemy
    delete_query.delete(synchronize_session=False)
    # commit
    db.commit()
    # no need to refresh, synchronzie_session seems to have it built in

    # RETURN RESPONSE of 204 pass with DELETE.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
# haha remember, DONT need to CONVERT id:int to STRING and %s to sanitze code for SQL queries with ALCHEMY
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    update_query = db.query(models.Post).filter(models.Post.id == id)

# to check/grab that specific post/query
    check_update_query = update_query.first()  # grabs the if exists

    # check to see if it exists
    if check_update_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        # ? (variable) current_user = oath2.get_current_user
    if check_update_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # * CHAIN update method to update_query...  similar to just adding update() end of the previous line.
    # * basically passing ALL of the singular query so just post.dict(),
    # * synchronize_session=False to help modify/delete + refresh our query within db with alchemy
    update_query.update(post.dict(), synchronize_session=False)
    # commit
    db.commit()
    # no need to refresh, synchronzie_session seems to have it built in

    # RETURN RESPONSE of 204 pass with DELETE.| ELSE return data (.first() is appropriate for grabbing 1 query)
    return update_query.first()
