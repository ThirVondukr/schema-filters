from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from schema_filters.fields import FieldFilter

if TYPE_CHECKING:
    from schema_filters.schema import FilterHolder

T = TypeVar("T")


class FilterProtocol(Protocol[T]):
    def filter(
        self,
        query: T,
        filters: list[FilterHolder],
    ) -> T:
        ...

    def field_python_type(self, field: FieldFilter) -> None:
        ...
