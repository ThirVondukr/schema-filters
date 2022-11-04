import pytest
from _pytest.fixtures import SubRequest

from schema_filters.fields import Op, Operator
from schema_filters.naming import NameGenerator, SeparatorNameGenerator


@pytest.fixture(params=["__", "-", " "])
def separator(request: SubRequest) -> str:
    return request.param  # type: ignore


@pytest.fixture(params=list(Op))
def operator(request: SubRequest) -> Operator:
    return request.param.value  # type: ignore


@pytest.fixture
def name_generator(separator: str) -> NameGenerator:
    return SeparatorNameGenerator(separator=separator)


@pytest.mark.parametrize(
    "field_name",
    (
        "user",
        "id",
        "user__username",
    ),
)
def test_encode_decode(
    name_generator: NameGenerator, separator: str, field_name: str, operator: Operator
) -> None:
    encoded = name_generator.encode(field_name, operator)
    assert encoded == f"{field_name}{separator}{operator.name}"
    assert name_generator.decode(encoded) == (field_name, operator.name)


def test_invalid_separator() -> None:
    with pytest.raises(ValueError):
        SeparatorNameGenerator("_")
