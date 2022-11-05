from typing import TypeVar

from sqlalchemy import Select

from schema_filters.fields import FieldFilter, Op, Operator
from schema_filters.schema._protocol import FilterRequest

T = TypeVar("T", bound=Select)


class SqlalchemyFilter:
    @staticmethod
    def filter(
        query: T,
        filter: FilterRequest,
    ) -> T:
        for param in filter.params:
            operator: Operator = Op[param.operator_name].value
            query = query.where(operator.op(param.filter.target, param.value))

        if filter.order_by:
            query = query.order_by(*filter.order_by)
        return query

    def field_python_type(self, field: FieldFilter) -> None:
        field.python_type = field.target.type.python_type
