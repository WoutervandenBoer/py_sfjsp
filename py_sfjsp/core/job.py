from scipy import stats

from py_sfjsp.core.machine import Machine
from py_sfjsp.core.distributions import Distribution

class Mode:
    def __init__(self, machine: Machine, duration: Distribution):
        self.machine: Machine = machine
        self.duration: Distribution = duration

    def sample(self) -> float:
        return self.duration.sample()

    def get_nth_percentile(self, n: float) -> float:
        return self.duration.get_nth_percentile(n)


class Operation:
    def __init__(self, modes: list[Mode], operation_id: int):
        self.modes: list[Mode] = modes
        self.operation_id: int = operation_id


class Job:
    def __init__(self, operations: list[Operation], job_id: int):
        self.operations: list[Operation] = operations
        self.job_id: int = job_id
