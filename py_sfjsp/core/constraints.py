from numbers import Number
from abc import ABC
from py_sfjsp.core.job import Operation


class Constraint(ABC):
    pass


class PrecedenceConstraint(Constraint):
    """States that `op2` should start after `op1` ends with a specified delay range."""
    def __init__(self, op1: Operation, op2: Operation, min_delay: Number, max_delay: Number):
        self.op1 = op1
        self.op2 = op2
        self.min_delay = min_delay
        self.max_delay = max_delay


class SameMachineConstraint(Constraint):
    """States that `op1` and `op2` should be performed on the same machine."""
    def __init__(self, op1: Operation, op2: Operation):
        self.op1 = op1
        self.op2 = op2
