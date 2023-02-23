from datetime import datetime
from sqlalchemy.orm import Session
from db.models import DbComment, DbUser
from routers.schemas import CommentBase
from fastapi import HTTPException, status


def create(db: Session, request: CommentBase):
  new_comment = DbComment(
    text = request.text,
    username = request.username,
    post_id = request.post_id,
    timestamp = datetime.now()
  )
  db.add(new_comment)
  db.commit()
  db.refresh(new_comment)
  return new_comment



def get_all(db: Session, post_id: int):
  return db.query(DbComment).filter(DbComment.post_id == post_id).all()

def delete(db: Session, comment_id: int, user_id: int):
  comment = db.query(DbComment).filter(DbComment.id == comment_id).first()
  user = db.query(DbUser).filter(DbUser.id == user_id).first()
  if not comment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f'comment with id {comment_id} not found')
  if comment.username != user.username or not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='Only comment creator can delete comment')

  db.delete(comment)
  db.commit()
  return 'ok'