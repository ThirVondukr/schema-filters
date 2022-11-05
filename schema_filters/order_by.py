from __future__ import annotations

import dataclasses
from typing import Any, Protocol, Sequence, TypeVar

from sqlalchemy.orm import InstrumentedAttribute

T = TypeVar("T")


class SortByEncodeProtocol(Protocol[T]):
    def decode(
        self,
        param: str | None,
        order_by: OrderBy,
    ) -> Sequence[T]:
        ...


class SqlalchemyEncoder(SortByEncodeProtocol[InstrumentedAttribute[Any]]):
    def decode(
        self,
        param: str | None,
        order_by: OrderBy,
    ) -> Sequence[InstrumentedAttribute[Any]]:
        if not param:
            return []

        result = []
        params = param.split(",")
        fields_by_name = {field.name: field for field in order_by.fields}
        for param in params:
            param = param.strip()
            field = fields_by_name.get(param)
            if field is None:
                continue
            result.append(field)
        return result


@dataclasses.dataclass
class OrderBy:
    fields: Sequence[Any]
    coder: SortByEncodeProtocol[Any]
    field_name: str = "order_by"
