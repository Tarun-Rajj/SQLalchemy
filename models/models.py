from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
# from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)
    role_id= Mapped[int] = mapped_column(Integer,nullable=False)

class Task(db.Model):
    id = Mapped[int]= mapped_column(Integer, primary_key=True)
    title=Mapped[str] = mapped_column(String,nullable=False)
    status=Mapped[str] = mapped_column(String,nullable=False,default='Pending')


