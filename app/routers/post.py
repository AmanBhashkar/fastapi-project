from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, utils,oauth2
from ..db import get_db
from typing import Optional, List
from sqlalchemy import func
from sqlalchemy.orm import Session

my_posts = [{"title": "title of post", "content": "content of post","id": 1}]

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
) 

def find_post_byId(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@router.get("/",response_model=List[schemas.PostOut])
#@router.get("/")
def get_post(db:Session=Depends(get_db),limit:int =10,skip:int=0, search: Optional[str]=""):

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
    

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    return new_post
 

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db:Session=Depends(get_db)):
    #post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return post

@router.delete("/{id}")
def del_post(id:int, db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to Perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return post

@router.put("/{id}")
def update_post(id: int,update_post:schemas.PostCreate, db: Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"posts with {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to Perform requested action")
    
    post_query.update(update_post.dict(),synchronize_session=False)

    db.commit()

    return {"data":post_query.first()}
