import dataclasses
import enum
import operator
from functools import cached_property
from typing import Any, Sequence, Type


@dataclasses.dataclass
class Operator:
    name: str
    op: Any


class Op(enum.Enum):
    eq = Operator("eq", operator.eq)
    not_eq = Operator("not_eq", operator.ne)
    gt = Operator("gt", operator.gt)
    lt = Operator("lt", operator.lt)

    in_ = Operator("in", operator.contains)


@dataclasses.dataclass
class FieldFilter:
    target: Any
    operators: Sequence[Op]
    python_type: Type[Any] = dataclasses.field(init=False)
    name: str = dataclasses.field(init=False)
    alias: str | None = None

    @cached_property
    def public_name(self) -> str:
        name = self.alias or self.name
        if not name:
            raise ValueError
        return name
