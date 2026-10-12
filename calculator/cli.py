"""The CLI reads input, prints output, and keeps asking until exit or EOF."""

from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def main():
    # One shared history list for the whole session, created outside the loop.
    history = []
    # Strategy: each name maps to the function that does that job.
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
    }
    print("Calculator. Commands: add, subtract, multiply, divide A B; history; exit")
    while True:
        try:
            words = input("> ").split()
        except EOFError:
            break
        if not words:
            continue
        command_name = words[0].lower()
        if command_name == "exit":
            break
        if command_name == "history":
            entries = HistoryCommand(history).execute()
            if entries:
                for entry in entries:
                    print(entry)
            else:
                print("History is empty.")
            continue
        if command_name not in operations:
            print(f"Unknown command: {command_name}. Try add, subtract, multiply, divide, history, or exit.")
            continue
        if len(words) != 3:
            print(f"{command_name} needs exactly two numbers, for example: {command_name} 5 3")
            continue
        try:
            a = float(words[1])
            b = float(words[2])
        except ValueError:
            print("Invalid number. Please enter numbers like 5, -2, or 3.5.")
            continue
        # Path for "add 5 3": read input -> choose Operations.add (strategy)
        # -> create a calculation with the factory -> create and execute a
        # command (which records history) -> print the answer.
        operation = operations[command_name]
        calculation = ArithmeticCalculation.create(a, b, operation)
        command = CalculateCommand(calculation, history, " ".join(words))
        try:
            result = command.execute()
        except ValueError as error:
            print(f"Error: {error}")
            continue
        print(result)