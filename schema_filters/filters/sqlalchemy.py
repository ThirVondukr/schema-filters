from typing import Any, Sequence, Tuple, TypeVar

from sqlalchemy import Select

from schema_filters.fields import FieldFilter, Op, Operator
from schema_filters.schema import FilterHolder

TTuple = TypeVar("TTuple", bound=Tuple[Any, ...])


class SqlalchemyFilter:
    @staticmethod
    def filter(
        query: Select[TTuple],
        filters: Sequence[FilterHolder],
    ) -> Select[TTuple]:
        for filter in filters:
            operator: Operator = Op[filter.operator_name].value
            query = query.where(operator.op(filter.filter.target, filter.value))
        return query

    def field_python_type(self, field: FieldFilter) -> None:
        field.python_type = field.target.type.python_type
