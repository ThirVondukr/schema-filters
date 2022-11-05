from typing import Any, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from schema_filters.fields import FieldFilter, Op
from schema_filters.filter import Filter
from schema_filters.filters.sqlalchemy import SqlalchemyFilter
from schema_filters.order_by import OrderBy, SqlalchemyEncoder
from schema_filters.schema.pydantic import PydanticGenerator


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


class UserFilter(Filter[User, Any]):
    __model__ = User
    __filter__ = SqlalchemyFilter()
    __schema_generator__ = PydanticGenerator()
    __order_by__ = OrderBy(
        fields=(User.id, User.username),
        coder=SqlalchemyEncoder(),
    )

    id = FieldFilter(User.id, (Op.eq, Op.not_eq))
    username = FieldFilter(User.username, (Op.eq,))


def test_should_be_present_on_schema() -> None:
    schema: Type[BaseModel] = UserFilter.schema()
    assert "order_by" in schema.__fields__


def test_apply_order_by() -> None:
    schema_cls: Type[BaseModel] = UserFilter.schema()
    schema = schema_cls(order_by="username, id")
    stmt = select(User)

    filtered = UserFilter.apply(stmt, schema)
    assert filtered.compare(stmt.order_by(User.username, User.id))
