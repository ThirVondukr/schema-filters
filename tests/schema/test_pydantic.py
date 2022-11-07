import pytest

from schema_filters.naming import NameGenerator, SeparatorNameGenerator
from schema_filters.order_by import OrderBy
from schema_filters.schema.pydantic import PydanticGenerator
from tests.testing import TestFieldCoder


@pytest.fixture
def name_generator() -> NameGenerator:
    return SeparatorNameGenerator(separator="__")


@pytest.fixture
def pydantic_generator() -> PydanticGenerator:
    return PydanticGenerator()


@pytest.mark.parametrize("title", ("", "UserFilter", "Title"))
def test_model_title(
    title: str,
    pydantic_generator: PydanticGenerator,
    name_generator: NameGenerator,
) -> None:
    schema = pydantic_generator.schema_class(
        title=title,
        filters=[],
        order_by=None,
        name_generator=name_generator,
    )
    assert schema.schema()["title"] == title


@pytest.mark.parametrize(
    "order_by",
    (
        OrderBy(fields=[], field_name="field-name=test", coder=TestFieldCoder()),
        OrderBy(fields=[], coder=TestFieldCoder()),
        OrderBy(fields=["id", "username"], coder=TestFieldCoder()),
        OrderBy(fields=["username", "username"], coder=TestFieldCoder()),
        OrderBy(fields=["username"], coder=TestFieldCoder()),
    ),
)
def test_order_by_constraint(
    order_by: OrderBy,
    pydantic_generator: PydanticGenerator,
    name_generator: NameGenerator,
) -> None:
    schema = pydantic_generator.schema_class(
        title="Title",
        filters=[],
        order_by=order_by,
        name_generator=name_generator,
    )

    assert schema.schema()
    field_schema = schema.schema()["properties"][order_by.field_name]
    assert field_schema["type"] == "array"

    expected_type = {"type": "string"}
    if order_by.fields:
        expected_type["enum"] = sorted({field for field in order_by.fields})  # type: ignore[assignment]

    assert field_schema["items"] == expected_type
