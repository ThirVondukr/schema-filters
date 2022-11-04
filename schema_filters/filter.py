from typing import Any, ClassVar, Generic, Type, TypeVar

from .fields import FieldFilter
from .filters import FilterProtocol
from .naming import NameGenerator, SeparatorNameGenerator
from .schema import SchemaGenerator

TModel = TypeVar("TModel")
TSchema = TypeVar("TSchema")
T = TypeVar("T")


class Filter(Generic[TModel, TSchema]):
    __filter_spec__: ClassVar[list[FieldFilter]]

    __model__: Type[TModel]
    __name_generator__: NameGenerator = SeparatorNameGenerator("__")
    __filter__: FilterProtocol[Any]
    __schema_generator__: SchemaGenerator[TSchema]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__filters__"):
            cls.__filter_spec__ = []

        for key, field in cls.__dict__.items():
            if not isinstance(field, FieldFilter):
                continue

            if not hasattr(field, "name") is None:
                field.name = key
            cls.__filter__.field_python_type(field)
            cls.__filter_spec__.append(field)

    @classmethod
    def schema(cls) -> Type[TSchema]:
        return cls.__schema_generator__.schema_class(
            cls.__name__,
            cls.__filter_spec__,
            name_generator=cls.__name_generator__,
        )

    @classmethod
    def apply(cls, query: T, schema: TSchema) -> T:
        filters = cls.__schema_generator__.filters_from_schema(
            schema=schema,
            filter_spec=cls.__filter_spec__,
            name_generator=cls.__name_generator__,
        )
        return cls.__filter__.filter(  # type: ignore
            query,
            filters,
        )
