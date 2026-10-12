"""CLI tests supply input with monkeypatch and check output with capsys."""

from calculator.cli import main


def run(monkeypatch, capsys, answers):
    # Feed the answers one at a time, as if typed, then return printed lines.
    responses = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))
    main()
    return capsys.readouterr().out.splitlines()


def test_four_operations(monkeypatch, capsys):
    lines = run(monkeypatch, capsys,
                ["add 5 3", "subtract 5 3", "multiply 5 3", "divide 6 4", "exit"])
    assert "8.0" in lines
    assert "2.0" in lines
    assert "15.0" in lines
    assert "1.5" in lines


def test_decimals_and_negatives(monkeypatch, capsys):
    lines = run(monkeypatch, capsys, ["add -2.5 1", "multiply -3 -4", "exit"])
    assert "-1.5" in lines
    assert "12.0" in lines


def test_history_shows_only_successes_in_order(monkeypatch, capsys):
    lines = run(monkeypatch, capsys,
                ["history", "add 5 3", "divide 1 0", "multiply 2 4", "history", "exit"])
    assert "History is empty." in lines
    assert lines[-2:] == ["add 5 3 = 8.0", "multiply 2 4 = 8.0"]


def test_unknown_command_then_continues(monkeypatch, capsys):
    lines = run(monkeypatch, capsys, ["power 2 3", "add 1 1", "exit"])
    assert any(line.startswith("Unknown command: power") for line in lines)
    assert "2.0" in lines


def test_wrong_operand_counts_then_continues(monkeypatch, capsys):
    lines = run(monkeypatch, capsys, ["add 5", "add 5 3 1", "add 2 2", "exit"])
    assert lines.count("add needs exactly two numbers, for example: add 5 3") == 2
    assert "4.0" in lines


def test_invalid_number_then_continues(monkeypatch, capsys):
    lines = run(monkeypatch, capsys, ["add five 3", "add 5 3", "exit"])
    assert "Invalid number. Please enter numbers like 5, -2, or 3.5." in lines
    assert "8.0" in lines


def test_divide_by_zero_then_continues(monkeypatch, capsys):
    lines = run(monkeypatch, capsys, ["divide 5 0", "divide 6 3", "exit"])
    assert "Error: Cannot divide by zero" in lines
    assert "2.0" in lines


def test_blank_line_and_uppercase(monkeypatch, capsys):
    lines = run(monkeypatch, capsys, ["", "ADD 1 2", "EXIT"])
    assert "3.0" in lines


def test_exit_stops_the_loop(monkeypatch, capsys):
    # If exit did not stop the loop, the answers would run out (StopIteration).
    lines = run(monkeypatch, capsys, ["exit"])
    assert lines[0].startswith("Calculator.")


def test_eof_ends_cleanly(monkeypatch, capsys):
    def end_of_input(prompt=""):
        raise EOFError
    monkeypatch.setattr("builtins.input", end_of_input)
    main()  # Must return without an uncaught exception.


def test_entry_point_imports_main():
    # Importing __main__ runs its import line; the guarded main() call is excluded.
    import calculator.__main__ as entry
    assert entry.main is main