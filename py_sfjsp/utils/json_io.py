import json
from typing import Dict, Any
from py_sfjsp.core.sfjsp import SFJSP
from py_sfjsp.core.job import Job, Operation, Mode
from py_sfjsp.core.machine import Machine
from py_sfjsp.core.constraints import Constraint, PrecedenceConstraint, SameMachineConstraint
from py_sfjsp.core.distributions import Distribution, LogNormalDistribution


def save_sfjsp_to_file(sfjsp: SFJSP, filepath: str) -> None:
    """
    Save an SFJSP object to a JSON file.

    Args:
        sfjsp: The SFJSP object to serialize
        filepath: Path to the output JSON file
    """

    def serialize_distribution(dist: Distribution) -> Dict[str, Any]:
        """Serialize a distribution object."""
        if isinstance(dist, LogNormalDistribution):
            return {
                "type": "LogNormalDistribution",
                "mu": dist.mu,
                "sigma": dist.sigma
            }
        else:
            raise ValueError(f"Unsupported distribution type: {type(dist)}")

    def serialize_mode(mode: Mode) -> Dict[str, Any]:
        """Serialize a Mode object."""
        return {
            "machine_id": mode.machine.machine_id,
            "duration": serialize_distribution(mode.duration)
        }

    def serialize_operation(operation: Operation) -> Dict[str, Any]:
        """Serialize an Operation object."""
        return {
            "operation_id": operation.operation_id,
            "modes": [serialize_mode(mode) for mode in operation.modes]
        }

    def serialize_job(job: Job) -> Dict[str, Any]:
        """Serialize a Job object."""
        return {
            "job_id": job.job_id,
            "operations": [serialize_operation(op) for op in job.operations]
        }

    def serialize_machine(machine: Machine) -> Dict[str, Any]:
        """Serialize a Machine object."""
        return {
            "machine_id": machine.machine_id
        }

    def serialize_constraint(constraint: Constraint) -> Dict[str, Any]:
        """Serialize a Constraint object."""
        if isinstance(constraint, PrecedenceConstraint):
            return {
                "type": "PrecedenceConstraint",
                "op1_id": constraint.op1.operation_id,
                "op2_id": constraint.op2.operation_id,
                "min_delay": constraint.min_delay,
                "max_delay": constraint.max_delay
            }
        elif isinstance(constraint, SameMachineConstraint):
            return {
                "type": "SameMachineConstraint",
                "op1_id": constraint.op1.operation_id,
                "op2_id": constraint.op2.operation_id
            }
        else:
            raise ValueError(f"Unsupported constraint type: {type(constraint)}")

    # Build the main dictionary
    sfjsp_dict = {
        "jobs": [serialize_job(job) for job in sfjsp.jobs],
        "machines": [serialize_machine(machine) for machine in sfjsp.machines],
        "constraints": [serialize_constraint(constraint) for constraint in sfjsp.constraints]
    }

    with open(filepath, 'w') as f:
        json.dump(sfjsp_dict, f, indent=2)


def load_sfjsp_from_file(filepath: str) -> SFJSP:
    """
    Load an SFJSP object from a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        SFJSP object reconstructed from JSON file
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    def deserialize_distribution(dist_data: Dict[str, Any]) -> Distribution:
        """Deserialize a distribution object."""
        if dist_data["type"] == "LogNormalDistribution":
            return LogNormalDistribution(dist_data["mu"], dist_data["sigma"])
        else:
            raise ValueError(f"Unsupported distribution type: {dist_data['type']}")

    # First pass: create machines and store them in a lookup dict
    machines = {}
    for machine_data in data["machines"]:
        machine = Machine(machine_data["machine_id"])
        machines[machine.machine_id] = machine

    # Second pass: create jobs and operations
    jobs = []
    operations_lookup = {}

    for job_data in data["jobs"]:
        operations = []
        for op_data in job_data["operations"]:
            modes = []
            for mode_data in op_data["modes"]:
                machine = machines[mode_data["machine_id"]]
                duration = deserialize_distribution(mode_data["duration"])
                mode = Mode(machine, duration)
                modes.append(mode)

            operation = Operation(modes, op_data["operation_id"])
            operations.append(operation)
            operations_lookup[operation.operation_id] = operation

        job = Job(operations, job_data["job_id"])
        jobs.append(job)

    # Third pass: create constraints
    constraints = []
    for constraint_data in data["constraints"]:
        if constraint_data["type"] == "PrecedenceConstraint":
            op1 = operations_lookup[constraint_data["op1_id"]]
            op2 = operations_lookup[constraint_data["op2_id"]]
            constraint = PrecedenceConstraint(
                op1,
                op2,
                constraint_data["min_delay"],
                constraint_data["max_delay"]
            )
        elif constraint_data["type"] == "SameMachineConstraint":
            op1 = operations_lookup[constraint_data["op1_id"]]
            op2 = operations_lookup[constraint_data["op2_id"]]
            constraint = SameMachineConstraint(op1, op2)
        else:
            raise ValueError(f"Unsupported constraint type: {constraint_data['type']}")

        constraints.append(constraint)

    return SFJSP(jobs, list(machines.values()), constraints)