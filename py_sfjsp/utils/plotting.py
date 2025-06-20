from py_sfjsp.core.sfjsp import SFJSP
from py_sfjsp.core.constraints import PrecedenceConstraint, SameMachineConstraint
from py_sfjsp.core.distributions import LogNormalDistribution


def print_sfjsp(sfjsp: SFJSP) -> None:
    """
    Print SFJSP in a multi-panel layout showing all key information.

    Args:
        sfjsp: The SFJSP object to display
    """

    def print_separator(title: str, width: int = 60):
        """Print a section separator with title."""
        padding = (width - len(title) - 2) // 2
        print("=" * width)
        print("=" + " " * padding + title + " " * padding + "=")
        print("=" * width)

    def format_distribution(dist) -> str:
        """Format distribution for display."""
        if isinstance(dist, LogNormalDistribution):
            return f"LogNorm(μ={dist.mu:.2f}, σ={dist.sigma:.2f})"
        return str(type(dist).__name__)

    # Panel 1: Jobs and Operations
    print_separator("JOBS & OPERATIONS")
    for job in sfjsp.jobs:
        print(f"Job {job.job_id}:")
        for i, op in enumerate(job.operations):
            arrow = " → " if i > 0 else "   "
            print(f"{arrow}Op {op.operation_id} ({len(op.modes)} modes)")
            for j, mode in enumerate(op.modes):
                prefix = "    ├─" if j < len(op.modes) - 1 else "    └─"
                duration_str = format_distribution(mode.duration)
                print(f"{prefix} Machine {mode.machine.machine_id}: {duration_str}")
        print()

    # Panel 2: Machines
    print_separator("MACHINES")
    machine_ops = {}  # Track which operations can run on each machine
    for job in sfjsp.jobs:
        for op in job.operations:
            for mode in op.modes:
                mid = mode.machine.machine_id
                if mid not in machine_ops:
                    machine_ops[mid] = []
                machine_ops[mid].append(op.operation_id)

    for machine in sorted(sfjsp.machines, key=lambda m: m.machine_id):
        ops = machine_ops.get(machine.machine_id, [])
        ops_str = ", ".join(f"Op{op}" for op in sorted(ops)) if ops else "No operations"
        print(f"Machine {machine.machine_id}: {ops_str}")
    print()

    # Panel 3: Constraints
    print_separator("CONSTRAINTS")
    if not sfjsp.constraints:
        print("No constraints defined")
    else:
        prec_constraints = [c for c in sfjsp.constraints if isinstance(c, PrecedenceConstraint)]
        same_machine_constraints = [c for c in sfjsp.constraints if isinstance(c, SameMachineConstraint)]

        if prec_constraints:
            print("Precedence Constraints:")
            for i, c in enumerate(prec_constraints, 1):
                delay_str = f"[{c.min_delay}-{c.max_delay}]" if c.min_delay != c.max_delay else f"[{c.min_delay}]"
                print(f"  {i}. Op{c.op1.operation_id} → Op{c.op2.operation_id} {delay_str}")
            print()

        if same_machine_constraints:
            print("Same Machine Constraints:")
            for i, c in enumerate(same_machine_constraints, 1):
                print(f"  {i}. Op{c.op1.operation_id} ≡ Op{c.op2.operation_id} (same machine)")
            print()

    # Panel 4: Problem Summary
    print_separator("PROBLEM SUMMARY")
    total_ops = sum(len(job.operations) for job in sfjsp.jobs)
    total_modes = sum(len(op.modes) for job in sfjsp.jobs for op in job.operations)
    flexibility = total_modes / total_ops if total_ops > 0 else 0

    print(f"Jobs:                {len(sfjsp.jobs)}")
    print(f"Operations:          {total_ops}")
    print(f"Machines:            {len(sfjsp.machines)}")
    print(f"Total Modes:         {total_modes}")
    print(f"Avg Flexibility:     {flexibility:.2f} modes/operation")
    print(f"Constraints:         {len(sfjsp.constraints)}")

    # Panel 5: Job Flow Diagram
    print_separator("JOB FLOWS")
    for job in sfjsp.jobs:
        flow = " → ".join(f"Op{op.operation_id}" for op in job.operations)
        machines_per_op = []
        for op in job.operations:
            machine_ids = sorted(mode.machine.machine_id for mode in op.modes)
            if len(machine_ids) == 1:
                machines_per_op.append(f"M{machine_ids[0]}")
            else:
                machines_per_op.append(f"M{{{','.join(map(str, machine_ids))}}}")

        machine_flow = " → ".join(machines_per_op)
        print(f"Job {job.job_id}: {flow}")
        print(f"         {machine_flow}")
        print()

    print("=" * 60)