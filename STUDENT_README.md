# My calculator submission

A command-line calculator in Python that uses static, class, and instance methods, an abstract class, and the Factory, Command, and Strategy patterns, with tests at 100% line coverage.

## Setup, run, and test

Requires Python 3.12 or newer.

bash
git clone https://github.com/ac2928/is218-calculator-patterns.git
cd is218-calculator-patterns
python3 -m venv .venv
source .venv/bin/activate          
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m calculator               
python -m pytest --cov=calculator --cov-report=term-missing --cov-fail-under=100


## Example conversation


Calculator. Commands: add, subtract, multiply, divide A B; history; exit
> add 5 3
8.0
> subtract 2.5 4
-1.5
> multiply -2 3
-6.0
> divide 6 0
Error: Cannot divide by zero
> power 2 3
Unknown command: power. Try add, subtract, multiply, divide, history, or exit.
> add 5
add needs exactly two numbers, for example: add 5 3
> add five 3
Invalid number. Please enter numbers like 5, -2, or 3.5.
> history
add 5 3 = 8.0
subtract 2.5 4 = -1.5
multiply -2 3 = -6.0
> exit


The failed division is not in history. Ctrl+D (end of input) also exits cleanly.

## Static, class, and instance methods

- **Static:** Operations.add, subtract, multiply, and divide use only the two numbers passed in, so they need no self or cls.
- **Class:** Calculation.create(cls, a, b, operation) receives cls, the class that called it, and builds a new object of that class.
- **Instance:** ArithmeticCalculation.execute(self) uses this objects own self.a , self.b, and self.operation. CalculateCommand.execute and HistoryCommand.execute are also instance methods.

## Factory, Command, and Strategy

- **Strategy:** the four Operations functions are the strategies. In cli.py, the operations dictionary picks one by name, for example "add" gives Operations.add.
- **Factory:** ArithmeticCalculation.create(a, b, operation) builds the calculation.
- **Command:** CalculateCommand runs a calculation and records it in history; HistoryCommand returns the history.

Trace of add 5 3: cli.main() reads the line and splits it into add, 5, 3 -> checks that add is in the dictionary and that there are two numbers -> converts them with float() -> selects Operations.add (Strategy) -> ArithmeticCalculation.create(5.0, 3.0, Operations.add) (Factory) -> CalculateCommand(calculation, history, "add 5 3").execute() (Command) -> the calculation's execute() returns 8.0 -> the command adds add 5 3 = 8.0 to history and returns 8.0 -> the CLI prints it.

## OOP

- **Encapsulation:** a Calculation keeps its two numbers and its operation together in self.a, self.b, and self.operation. HistoryCommand.execute() returns a copy of the history list, so code that receives it cannot add to or remove from the stored list.
- **Abstraction:** Calculation is an abstract class whose @abstractmethod execute() is a promise that every concrete calculation must provide execute(). Calculation itself cannot be created.
- **Inheritance:** ArithmeticCalculation inherits __init__ and the create() factory from Calculation and only adds its own execute().
- **Polymorphism:** CalculateCommand simply calls self.calculation.execute(). It works with any Calculation subclass that keeps the execute() contract, without knowing which one it is.
- **Composition:** a CalculateCommand holds a calculation and the history list; a calculation holds an operation function.

## SOLID

- **Single responsibility:** Operations does arithmetic, ArithmeticCalculation runs one calculation, CalculateCommand coordinates running and recording, HistoryCommand returns history, and cli.py handles input and printing.
- **Open/closed:** a new operation only needs a new static method in Operations and one new entry in the CLI dictionary. ArithmeticCalculation.execute() and CalculateCommand.execute() do not change.
- **Liskov substitution:** any Calculation subclass can replace ArithmeticCalculation in CalculateCommand as long as its execute() returns a number or raises an appropriate error such as ValueError.
- **Interface segregation:** a calculation only has to provide execute(), and each command has just one execute() method.
- **Dependency inversion:** CalculateCommand receives a Calculation instead of building one, and a calculation receives its operation instead of hard-coding addition.

**Adding subtraction, multiplication, and division:** the starter only had add. I added subtract, multiply, and divide as static methods and registered them in the CLI dictionary. ArithmeticCalculation.execute() did not change, because it already runs whatever operation it was given with self.operation(self.a, self.b).

## Tests and GitHub Actions

Successful Actions run: https://github.com/ac2928/is218-calculator-patterns/actions/runs/38264142122

The tests pass with 100% line coverage of the calculator package. They cover all four operations (normal values, decimals, negatives, zero), division by zero, the factory, the abstract class, calculations with different operations, both commands (result, history entry, no entry after a failure, empty history, and the returned copy), and the CLI (success, unknown commands, wrong operand counts, invalid numbers, division by zero, continuing after errors, exit, and EOF).

## Coverage exclusions

- Calculation.execute() in calculation.py: the abstract placeholder only declares the contract and has no behavior to test.
- The if __name__ == "__main__": block in __main__.py: it only calls main(), and main() is tested directly in tests/test_cli.py.

Nothing else is excluded. Arithmetic, the factory, commands, history, input parsing, and error handling are all covered by tests.