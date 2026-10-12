"""Arithmetic strategies: each static method needs only the two numbers it is given."""


class Operations:
    @staticmethod
    def add(a: float, b: float) -> float:
        # This method uses only a and b. No object state is needed.
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        # Check first so the CLI can show one clear message.
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
