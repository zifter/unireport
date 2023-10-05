import pytest

from unireport.utils import as_bool


@pytest.mark.parametrize(
    "value,expected",
    (
        ("f", False),
        ("t", True),
        (None, False),
        (True, True),
    ),
)
def test_as_bool(value, expected):
    assert as_bool(value) == expected
