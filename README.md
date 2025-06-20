# SFJSP: Stochastic Flexible Job-shop Scheduling Problem

This Python package provides a minimal framework for defining and working with the **Stochastic Flexible Job-shop Scheduling Problem (SFJSP)**.

> ❗ Note: This package does **not** include any solvers. It is intended as a lightweight data structure that helps you store, load and work with SFJSP problem instances.
> A schedule cannot even be defined here. That is up to you to add!

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