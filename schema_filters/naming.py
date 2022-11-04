from typing import Protocol

from schema_filters.fields import Op, Operator


class NameGenerator(Protocol):
    def encode(self, filter_name: str, operator: Operator) -> str:
        ...

    def decode(self, field_name: str) -> tuple[str, str]:
        ...


class SeparatorNameGenerator:
    def __init__(self, separator: str = "__") -> None:
        self.separator = separator
        self.__sanity_check()

    def __sanity_check(self) -> None:
        for operator in Op:
            if len(self.decode(operator.value.name)) > 1:
                raise ValueError(
                    f'{self.__class__.__name__}: "{self.separator}" cannot be used as separator'
                    f"since it splits {operator} name"
                )

    def encode(self, filter_name: str, operator: Operator) -> str:
        return f"{filter_name}{self.separator}{operator.name}"

    def decode(self, name: str) -> tuple[str, str]:
        return tuple(name.rsplit(self.separator, maxsplit=1))  # type: ignore
