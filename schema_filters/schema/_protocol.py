import dataclasses
from typing import Any, NamedTuple, Protocol, Type, TypeVar

from schema_filters.fields import FieldFilter
from schema_filters.naming import NameGenerator
from schema_filters.order_by import OrderBy

T = TypeVar("T")


class FilterParameter(NamedTuple):
    filter: FieldFilter
    field_name: str
    operator_name: str
    value: Any


@dataclasses.dataclass
class FilterRequest:
    params: list[FilterParameter]
    order_by: list[Any] | None


class SchemaGenerator(Protocol[T]):
    def schema_class(
        self,
        title: str,
        filters: list[FieldFilter],
        order_by: OrderBy | None,
        name_generator: NameGenerator,
    ) -> Type[T]:
        ...

    def filters_from_schema(
        self,
        schema: T,
        filter_spec: list[FieldFilter],
        order_by: OrderBy | None,
        name_generator: NameGenerator,
    ) -> FilterRequest:
        ...
