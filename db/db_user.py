from fastapi import HTTPException, status
from db.models import DbUser, DbPost
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash

def create_user(db: Session, request: UserBase):
  new_user = DbUser(
    username = request.username,
    email = request.email,
    password = Hash.bcrypt(request.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user

def user_stats(db:Session, id: int, user_id:int):
  posts = db.query(DbPost).filter(DbPost.user_id == id).all()
  #comments = db.query(DbComment).filter(DbComment.post_id == id).all()
  #TODO: join con posts para el total de comentarios
  
  stats = {
    'sum_posts': len(posts),
    #'sum_comments': len(comments),
  }

  return stats;