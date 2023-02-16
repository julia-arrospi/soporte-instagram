from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
import datetime

user_followers = Table(
  'user_followers',
  Base.metadata,
  Column('user_id', Integer, ForeignKey('user.id')),
  Column('follower_id', Integer, ForeignKey('user.id')),
  Column('timestamp', DateTime, default=datetime.datetime.utcnow),
)
class DbUser(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)
  items = relationship('DbPost', back_populates='user')
  #relaciones muchos a muchos sobre si mismo
  followers=relationship(
    'DbUser', 
    secondary=user_followers,
    primaryjoin=id == user_followers.c.user_id,
    secondaryjoin=id == user_followers.c.follower_id,
    )
  following=relationship(
    'DbUser', 
    secondary=user_followers,
    primaryjoin=id == user_followers.c.follower_id,
    secondaryjoin=id == user_followers.c.user_id,
    )

class DbPost(Base):
  __tablename__ = 'post'
  id = Column(Integer, primary_key=True, index=True)
  image_url = Column(String)
  image_url_type = Column(String)
  caption = Column(String)
  timestamp = Column(DateTime)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('DbUser', back_populates='items')
  comments = relationship('DbComment', back_populates='post')

class DbComment(Base):
  __tablename__ = 'comment'
  id = Column(Integer, primary_key=True, index=True)
  text = Column(String)
  username = Column(String)
  timestamp = Column(DateTime)
  post_id = Column(Integer, ForeignKey('post.id'))
  post = relationship("DbPost", back_populates="comments")