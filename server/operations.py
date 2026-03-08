from abc import ABC, abstractmethod

# This class only exists to define rules for others.
class Operation(ABC):
    
    # RULE 1: Every operation MUST have a 'calculate' method.
    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        pass
    
    # RULE 2: Every operation MUST define its own symbol
    @property
    @abstractmethod
    def symbol(self) -> str:
        pass


class Addition(Operation):
    symbol = "+"

    def calculate(self, a: float, b: float) -> float:
        return a + b


class Subtraction(Operation):
    symbol = "-"

    def calculate(self, a: float, b: float) -> float:
        return a - b


class Multiplication(Operation):
    symbol = "*"

    def calculate(self, a: float, b: float) -> float:
        return a * b


class Division(Operation):
    symbol = "/"

    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b


# Registry: maps the string a client sends to the matching Operation instance.
OPERATIONS: dict[str, Operation] = {
    "+": Addition(),
    "-": Subtraction(),
    "*": Multiplication(),
    "/": Division(),
}
