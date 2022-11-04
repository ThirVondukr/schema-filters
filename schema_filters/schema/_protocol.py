from typing import Any, NamedTuple, Protocol, Type, TypeVar

from schema_filters.fields import FieldFilter
from schema_filters.naming import NameGenerator

T = TypeVar("T")


class FilterHolder(NamedTuple):
    filter: FieldFilter
    field_name: str
    operator_name: str
    value: Any


class SchemaGenerator(Protocol[T]):
    def schema_class(
        self,
        title: str,
        filters: list[FieldFilter],
        name_generator: NameGenerator,
    ) -> Type[T]:
        ...

    def filters_from_schema(
        self,
        schema: T,
        filter_spec: list[FieldFilter],
        name_generator: NameGenerator,
    ) -> list[FilterHolder]:
        ...
