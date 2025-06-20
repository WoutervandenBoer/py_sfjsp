from py_sfjsp.core.constraints import Constraint
from py_sfjsp.core.job import Job
from py_sfjsp.core.machine import Machine


class SFJSP:
    def __init__(self, jobs: list[Job], machines: list[Machine], constraints: list[Constraint]):
        self.jobs: list[Job] = jobs
        self.machines: list[Machine] = machines
        self.constraints: list[Constraint] = constraints

