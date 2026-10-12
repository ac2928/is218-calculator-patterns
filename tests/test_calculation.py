"""The factory builds a concrete calculation; each calculation runs its own operation."""

import pytest

from calculator.calculation import ArithmeticCalculation, Calculation
from calculator.operations import Operations


@pytest.mark.parametrize("operation, expected", [
    (Operations.add, 8),
    (Operations.subtract, 2),
    (Operations.multiply, 15),
    (Operations.divide, 5 / 3),
])
def test_calculation_uses_each_operation_function(operation, expected):
    calculation = ArithmeticCalculation.create(5, 3, operation)
    assert isinstance(calculation, ArithmeticCalculation)
    assert calculation.operation is operation
    assert calculation.execute() == pytest.approx(expected)


def test_factory_creates_separate_objects():
    first = ArithmeticCalculation.create(1, 2, Operations.add)
    second = ArithmeticCalculation.create(10, 20, Operations.add)
    assert first is not second
    assert (first.a, first.b) == (1, 2)
    assert (second.a, second.b) == (10, 20)


def test_calculation_passes_divide_by_zero_error_along():
    calculation = ArithmeticCalculation.create(5, 0, Operations.divide)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation.execute()


def test_abstract_class_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Calculation(5, 3, Operations.add)