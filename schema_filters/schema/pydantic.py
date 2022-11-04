from typing import Any, Type

import pydantic
from pydantic import BaseModel

from schema_filters.fields import FieldFilter
from schema_filters.naming import NameGenerator
from schema_filters.schema import FilterHolder


class PydanticGenerator:
    def schema_class(
        self,
        title: str,
        filters: list[FieldFilter],
        name_generator: NameGenerator,
    ) -> Type[BaseModel]:
        model_fields: Any = {}
        for filter_ in filters:
            for operator in filter_.operators:
                field_name = name_generator.encode(filter_.public_name, operator.value)
                model_fields[field_name] = (filter_.python_type, None)

        return pydantic.create_model(title, **model_fields)

    def filters_from_schema(
        self,
        schema: BaseModel,
        filter_spec: list[FieldFilter],
        name_generator: NameGenerator,
    ) -> list[FilterHolder]:
        filters: list[FilterHolder] = []
        for key, value in schema.dict(exclude_unset=True).items():
            field_name, operator_name = name_generator.decode(key)
            field_filter = next(f for f in filter_spec if f.public_name == field_name)
            holder = FilterHolder(
                filter=field_filter,
                field_name=field_name,
                operator_name=operator_name,
                value=value,
            )
            filters.append(holder)
        return filters
