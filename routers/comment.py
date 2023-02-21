from routers.schemas import CommentBase, UserAuth
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from auth.oauth2 import get_current_user
from mail import mail
from db.models import DbPost, DbUser

router = APIRouter(
  prefix='/comment',
  tags=['comment']
)

@router.get('/all/{post_id}')
def comments(post_id: int, db: Session = Depends(get_db)):
  return db_comment.get_all(db, post_id)


@router.post('')
def create(request: CommentBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    post = db.query(DbPost).filter(DbPost.id == request.post_id).first()
    creator_post = db.query(DbUser).filter(DbUser.id == post.user_id).first()
    mail.send_mail(creator_post.email, creator_post.username, request.username, request.text)
    return db_comment.create(db, request)
