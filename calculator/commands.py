"""Commands represent actions. Each one has an execute() method."""

from calculator.calculation import Calculation


class CalculateCommand:
    def __init__(self, calculation: Calculation, history: list[str], label: str = ""):
        # The command receives its pieces instead of building them.
        self.calculation = calculation
        self.history = history
        self.label = label

    def execute(self) -> float:
        # Run the math first. If it raises, the next line never runs,
        # so a failed calculation is never added to history.
        result = self.calculation.execute()
        self.history.append(f"{self.label} = {result}")
        return result


class HistoryCommand:
    def __init__(self, history: list[str]):
        # Shares the same history list that CalculateCommand adds to.
        self.history = history

    def execute(self) -> list[str]:
        # Return a copy so callers cannot change the stored list.
        return list(self.history)