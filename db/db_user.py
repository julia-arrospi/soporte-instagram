from fastapi import HTTPException, status
from db.models import DbUser, DbPost, DbComment, user_followers
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash
import datetime

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

def follow(db: Session, user_id:int, follower_id:int):
  if follower_id == user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='You cannot follow yourself')

  user = db.query(DbUser).filter(DbUser.id == user_id).first()
  follower = db.query(DbUser).filter(DbUser.id == follower_id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {user_id} not found')

  if not follower:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {follower_id} not found')
    
  user.followers.append(follower)
  db.commit()
  db.refresh(user)
  return user

def user_stats(db:Session, id: int, user_id:int):
  if id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
      detail='Only logged user can see stats.')
  posts = db.query(DbPost).filter(DbPost.user_id == id).all()
  comments = db.query(DbComment).join(DbPost).filter(DbPost.user_id == id).all()
  
  today = datetime.datetime.now()
  last_week = today - datetime.timedelta(days = 7)
  last_last_week = today - datetime.timedelta(days = 14)

  #first = today.replace(day=1)
  #last_month = first - datetime.timedelta(days=1)

  # cant comentarios + promedio por semana
  comments_last_week = db.query(DbComment).join(DbPost).filter(DbPost.user_id == id).filter(DbComment.timestamp <= last_week).filter(DbComment.timestamp >= last_last_week).all()
  comments_this_week = db.query(DbComment).join(DbPost).filter(DbPost.user_id == id).filter(DbComment.timestamp <= today).filter(DbComment.timestamp >= last_week).all()

  if(len(comments_last_week) == 0):
    comments_percentage_this_week = len(comments_this_week)*100
  elif(len(comments_last_week) == len(comments_this_week)):
    comments_percentage_this_week = 0
  else:
    comments_percentage_this_week = len(comments_this_week)*100/len(comments_last_week)
  
  # cant seguidores + promedio por semana (agregar timestamp)
  followers_last_week = db.query(user_followers.c.timestamp).filter(user_followers.c.user_id==id).filter(user_followers.c.timestamp <= last_week).filter(user_followers.c.timestamp>=last_last_week).all()
  followers_this_week = db.query(user_followers.c.timestamp).filter(user_followers.c.user_id==id).filter(user_followers.c.timestamp <= today).filter(user_followers.c.timestamp>=last_week).all()
  
  if(len(followers_last_week) == 0):
    followers_percentage_this_week = len(followers_this_week)*100
  elif(len(followers_last_week) == len(followers_this_week)):
    followers_percentage_this_week = 0
  else:
    followers_percentage_this_week = len(followers_this_week)*100/len(followers_last_week)

  if(len(comments_this_week) > len(comments_last_week)):
    avg_comments = '+'
  else:
    avg_comments = '-'

  if(len(followers_this_week) > len(followers_last_week)):
    avg_followers = '+'
  else:
    avg_followers = '-'
  
  stats = {
    'sum_posts': len(posts),
    'sum_comments': len(comments),
    'comments_last_week': len(comments_last_week),
    'comments_this_week': len(comments_this_week),
    'avg_comments_this_week': avg_comments + str(comments_percentage_this_week) + '%',
    'followers_last_week': len(followers_last_week),
    'followers_this_week': len(followers_this_week),
    'avg_followers_this_week': avg_followers + str(followers_percentage_this_week) + '%'
  }

  return stats;

def user_profile(db:Session, id: int):
  user = db.query(DbUser).filter(DbUser.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {id} not found')

  return user;