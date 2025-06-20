import os
from py_sfjsp.utils.json_io import load_sfjsp_from_file
from py_sfjsp.utils.plotting import print_sfjsp


def main():
    json_path = os.path.join(os.path.dirname(__file__), "instances", "basic_sfjsp.sfjsp")

    my_sfjsp = load_sfjsp_from_file(json_path)

    # lets print some individual components
    print("all machines:", my_sfjsp.machines, "\n")

    job = my_sfjsp.jobs[0] # take the first job for printing
    print("some job id:", job.job_id, "\n")

    op = job.operations[0] # take the first operation of job for printing
    print("some operation id:",op.operation_id, "\n")

    mode = op.modes[0] # take the first mode of operation for printing

    print("machine id for some mode:",mode.machine.machine_id)
    print("duration of the mode:", mode.duration)
    print("sample the mode duration:",mode.sample())
    print("50th percentile mode duration:",mode.get_nth_percentile(50))
    print("90th percentile mode duration:",mode.get_nth_percentile(90))

    print("now lets do the nicely formatted print statement :)")
    print_sfjsp(my_sfjsp)


if __name__ == "__main__":
    main()