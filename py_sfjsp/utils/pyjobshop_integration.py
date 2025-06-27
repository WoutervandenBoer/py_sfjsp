from pyjobshop import Model

from py_sfjsp.core.constraints import PrecedenceConstraint, SameMachineConstraint
from py_sfjsp.core.sfjsp import SFJSP


def get_pyjobshop_model(sfjsp_instance: SFJSP, percentile_value: float):
    # TODO: investigate the type annotations, e.g., task1 & task2 are expected to be of type pyjobshop.Task,
    # yet find_task_by_operation_id returns an int. But this is odd, as it simply returns an element from job.tasks...
    model = Model()

    # Add machines to the model
    machines = {machine.machine_id: model.add_machine(name=f"Machine {machine.machine_id}") for machine in
                sfjsp_instance.machines}

    # Add jobs and tasks to the model
    for job in sfjsp_instance.jobs:
        pyjobshop_job = model.add_job(name=f"Job {job.job_id}")
        for operation in job.operations:
            pyjobshop_task = model.add_task(pyjobshop_job, name=f"Task {operation.operation_id}")

            # Add modes for each possible machine
            for mode in operation.modes:
                machine = machines[mode.machine.machine_id]
                duration = mode.get_nth_percentile(percentile_value)
                model.add_mode(pyjobshop_task, machine, duration)

    # Add constraints to the model
    for constraint in sfjsp_instance.constraints:
        if isinstance(constraint, PrecedenceConstraint):
            task1 = find_task_by_operation_id(model, constraint.op1.operation_id)
            task2 = find_task_by_operation_id(model, constraint.op2.operation_id)
            model.add_end_before_start(task1, task2, delay=constraint.min_delay)
            # Handle max_delay if necessary
        elif isinstance(constraint, SameMachineConstraint):
            task1 = find_task_by_operation_id(model, constraint.op1.operation_id)
            task2 = find_task_by_operation_id(model, constraint.op2.operation_id)
            model.add_identical_resources(task1, task2)

    return model


def find_task_by_operation_id(model: Model, operation_id: int):
    for job in model.jobs:
        for task in job.tasks:
            if f"Task {operation_id}" == task.name:
                return task
    raise ValueError(f"Task with operation ID {operation_id} not found")
