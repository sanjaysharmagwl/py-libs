import pytest

from pylibs_core import slugify


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("  already-slugged  ", "already-slugged"),
        ("Multiple   Spaces", "multiple-spaces"),
        ("", ""),
    ],
)
def test_slugify(value: str, expected: str) -> None:
    assert slugify(value) == expected


def test_slugify_custom_separator() -> None:
    assert slugify("Hello World", separator="_") == "hello_world"
