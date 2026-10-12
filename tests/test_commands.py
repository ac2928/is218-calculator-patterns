"""Commands coordinate the action and history; calculations do the math."""

import pytest

from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def test_calculate_command_returns_result_and_records_history():
    history = []
    calculation = ArithmeticCalculation.create(5, 3, Operations.add)
    command = CalculateCommand(calculation, history, "add 5 3")
    assert command.execute() == 8
    assert history == ["add 5 3 = 8"]


def test_failed_calculation_adds_no_history_entry():
    history = []
    calculation = ArithmeticCalculation.create(5, 0, Operations.divide)
    command = CalculateCommand(calculation, history, "divide 5 0")
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        command.execute()
    assert history == []


def test_history_keeps_successful_entries_in_order():
    history = []
    CalculateCommand(ArithmeticCalculation.create(5, 3, Operations.add), history, "add 5 3").execute()
    CalculateCommand(ArithmeticCalculation.create(5, 3, Operations.subtract), history, "subtract 5 3").execute()
    assert HistoryCommand(history).execute() == ["add 5 3 = 8", "subtract 5 3 = 2"]


def test_empty_history():
    assert HistoryCommand([]).execute() == []


def test_history_command_returns_a_copy():
    history = ["add 5 3 = 8"]
    copy = HistoryCommand(history).execute()
    copy.append("fake entry")
    copy.clear()
    assert history == ["add 5 3 = 8"]