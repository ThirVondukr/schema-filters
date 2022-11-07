from __future__ import annotations

import dataclasses
from functools import cached_property
from typing import Any, NamedTuple, Protocol, Sequence, TypeVar

from sqlalchemy.orm import InstrumentedAttribute

T = TypeVar("T")


class OrderByFieldWrapper(NamedTuple):
    name: str
    field: Any


class SortByEncodeProtocol(Protocol[T]):
    def decode(
        self,
        *,
        params: list[str] | None = None,
        order_by: OrderBy,
    ) -> Sequence[T]:
        ...

    def field_wrapper(self, field: T) -> OrderByFieldWrapper:
        ...


class SqlalchemyEncoder(SortByEncodeProtocol[InstrumentedAttribute[Any]]):
    def decode(
        self,
        *,
        params: list[str] | None = None,
        order_by: OrderBy,
    ) -> Sequence[InstrumentedAttribute[Any]]:
        params = params or []

        result = []
        fields_by_name = {field.name: field for field in order_by.fields}
        for parameter in params:
            field = fields_by_name.get(parameter)
            if field is None:
                continue
            result.append(field)
        return result

    def field_wrapper(self, field: InstrumentedAttribute[Any]) -> OrderByFieldWrapper:
        return OrderByFieldWrapper(
            field=field,
            name=field.name,
        )


@dataclasses.dataclass
class OrderBy:
    fields: Sequence[Any]
    coder: SortByEncodeProtocol[Any]
    field_name: str = "order_by"
    separator = ","

    @cached_property
    def wrapped_fields(self) -> Sequence[OrderByFieldWrapper]:
        return tuple(self.coder.field_wrapper(field) for field in self.fields)
