from typing import Any, Type

import pydantic
from pydantic import BaseModel

from schema_filters.fields import FieldFilter
from schema_filters.naming import NameGenerator
from schema_filters.order_by import OrderBy
from schema_filters.schema import FilterParameter
from schema_filters.schema._protocol import FilterRequest


class PydanticGenerator:
    def schema_class(
        self,
        title: str,
        filters: list[FieldFilter],
        order_by: OrderBy | None,
        name_generator: NameGenerator,
    ) -> Type[BaseModel]:
        model_fields: Any = {}
        if order_by:
            model_fields[order_by.field_name] = (str, pydantic.Field(default=None))

        for filter_ in filters:
            for operator in filter_.operators:
                field_name = name_generator.encode(filter_.public_name, operator.value)
                model_fields[field_name] = (filter_.python_type, None)

        return pydantic.create_model(title, **model_fields)

    def filters_from_schema(
        self,
        schema: BaseModel,
        filter_spec: list[FieldFilter],
        order_by: OrderBy | None,
        name_generator: NameGenerator,
    ) -> FilterRequest:
        params: list[FilterParameter] = []
        exclude = set()
        if order_by:
            exclude.add(order_by.field_name)

        for key, value in schema.dict(exclude_unset=True, exclude=exclude).items():
            field_name, operator_name = name_generator.decode(key)
            field_filter = next(f for f in filter_spec if f.public_name == field_name)
            param = FilterParameter(
                filter=field_filter,
                field_name=field_name,
                operator_name=operator_name,
                value=value,
            )
            params.append(param)

        order_by_param = None
        if order_by is not None:
            order_by_param = getattr(schema, order_by.field_name, None)
            order_by_param = order_by.coder.decode(order_by_param, order_by)

        return FilterRequest(
            params=params,
            order_by=order_by_param,
        )
