# SFJSP: Stochastic Flexible Job-shop Scheduling Problem

This Python package provides a minimal framework for defining and working with the **Stochastic Flexible Job-shop Scheduling Problem (SFJSP)**.

> ❗ Note: This package does **not** include any solvers. It is intended as a lightweight data structure that helps you store, load and work with SFJSP problem instances.
> A schedule cannot even be defined here. That is up to you!

---

## What is the SFJSP?

The Stochastic Flexible Job-shop Scheduling Problem (SFJSP) is an extension of the Flexible Job-shop Scheduling Problem with probabilistic operation durations.

In the SFJSP, each job contains various operations. Each operation needs to be scheduled on a machine. 
Operations all have durations, sometimes different for each machine that it can be scheduled on.

An SFJSP as defined in this package can be broken down into the following concepts:
- **Jobs**: Each `Job` consists of a sequence of operations.
- **Operations**: Each `Operation` can be processed on one of several machines (this is what the *flexibility* in SFJSP refers to).
- **Modes**: Each `Mode` represents a possible machine-choice for an operation, along with a stochastic duration.
- **Machines**: A `Machine` is a resource on which operations are processed.
- **Stochastic Durations**: Unlike deterministic scheduling problems, each operation duration is modeled as a probability distribution.
- **Constraints**:
  - `PrecedenceConstraint`: Defines ordering between two operations with delay.
  - `SameMachineConstraint`: States that two operations should be assigned to the same machine.


---
## Storing and Loading Instances
Instances are stored in json format. The functions in `sfjsp/utils/json_io.py` let you store and load an `SFJSP` object to/from such a file.

## Example Instances
Example problem instances can be found in `py_sfjsp/examples/instances/`.

## Example Usage
`sfjsp/examples/basic_example.py` loads a basic problem instance from a file and prints some facts about the instance.
```bash
python -m py_sfjsp.examples.basic_example
```
#### output:
```
============================================================
=                    JOBS & OPERATIONS                    =
============================================================
Job 1:
   Op 1 (2 modes)
    ├─ Machine 1: LogNorm(μ=1.00, σ=0.30)
    └─ Machine 2: LogNorm(μ=1.20, σ=0.40)
 → Op 2 (2 modes)
    ├─ Machine 2: LogNorm(μ=0.80, σ=0.20)
    └─ Machine 3: LogNorm(μ=0.90, σ=0.25)

Job 2:
   Op 3 (1 modes)
    └─ Machine 1: LogNorm(μ=1.50, σ=0.50)
 → Op 4 (1 modes)
    └─ Machine 3: LogNorm(μ=1.10, σ=0.35)

============================================================
=                         MACHINES                         =
============================================================
Machine 1: Op1, Op3
Machine 2: Op1, Op2
Machine 3: Op2, Op4

============================================================
=                       CONSTRAINTS                       =
============================================================
Precedence Constraints:
  1. Op1 → Op2 [0.5-10.0]
  2. Op3 → Op4 [0.0-5.0]

Same Machine Constraints:
  1. Op1 ≡ Op3 (same machine)

============================================================
=                     PROBLEM SUMMARY                     =
============================================================
Jobs:                2
Operations:          4
Machines:            3
Total Modes:         6
Avg Flexibility:     1.50 modes/operation
Constraints:         3
============================================================
=                        JOB FLOWS                        =
============================================================
Job 1: Op1 → Op2
         M{1,2} → M{2,3}

Job 2: Op3 → Op4
         M1 → M3

============================================================

```