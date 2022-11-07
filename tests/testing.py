from typing import Sequence

from schema_filters.order_by import OrderBy, OrderByFieldWrapper, SortByEncodeProtocol


class TestFieldCoder(SortByEncodeProtocol[str]):
    def decode(
        self,
        *,
        params: list[str] | None = None,
        order_by: OrderBy,
    ) -> Sequence[str]:
        return params or []

    def field_wrapper(self, field: str) -> OrderByFieldWrapper:
        return OrderByFieldWrapper(
            field=field,
            name=field,
        )
