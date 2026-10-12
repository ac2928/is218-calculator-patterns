"""Each static operation is called on the class, without creating an object."""

import pytest

from calculator.operations import Operations


@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2), (-5, 3, -8), (0, 0, 0), (2.5, 0.5, 2.0),
])
def test_subtract(a, b, expected):
    assert Operations.subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 15), (-5, 3, -15), (0, 7, 0), (1.5, 2, 3.0), (-2, -4, 8),
])
def test_multiply(a, b, expected):
    assert Operations.multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a, b, expected", [
    (6, 3, 2), (-6, 3, -2), (0, 5, 0), (7, 2, 3.5), (1, 3, 0.3333333),
])
def test_divide(a, b, expected):
    assert Operations.divide(a, b) == pytest.approx(expected)


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Operations.divide(5, 0)