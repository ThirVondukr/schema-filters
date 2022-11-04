from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from schema_filters.fields import FieldFilter, Op
from schema_filters.filter import Filter
from schema_filters.filters.sqlalchemy import SqlalchemyFilter
from schema_filters.schema.pydantic import PydanticGenerator


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]


class PostFilter(Filter[Post, Any]):
    __model__ = Post
    __filter__ = SqlalchemyFilter()
    __schema_generator__ = PydanticGenerator()

    id = FieldFilter(Post.id, (Op.eq, Op.not_eq))
    title = FieldFilter(Post.title, (Op.eq,))
    user_username = FieldFilter(User.username, (Op.eq,))
