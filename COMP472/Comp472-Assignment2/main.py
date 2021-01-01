import os
import glob
import time

from x_puzzle_solver import XPuzzleSolver


def start(puzzles, num_rows, timeout):
    """
    Start processing the sample puzzles.
    :param puzzles: The array of sample puzzles to solve.
    :param num_rows: The number of rows that each puzzle will have.
    :param timeout: The max number of seconds that each algorithm has to execute before being timed out.
    :return: void
    """
    # Create a new X-Puzzle solver object
    x_puzzle_solver = XPuzzleSolver(puzzles, num_rows, timeout)

    # Start the process
    x_puzzle_solver.solve()
# end: start


def read_samples(input_filename):
    """
    Read in the sample initial states.
    :param input_filename: The filename to use for reading-in the data.
    :return: The array of samples.
    """
    # Define an array to store the initial puzzle states
    initial_states = []

    # Read the sample initial-states from the input file line-by-line and add
    # each one into our array
    file = open(input_filename, "r")

    while True:
        # Get the next line from the file
        line = file.readline()

        # If the line is empty, we are done reading
        if not line:
            break

        # Write our sample initial-state to our array (strip out the newline character)
        initial_states.append(line.strip())
    # end: while

    # Don't forget to close our file connection
    file.close()

    return initial_states
# end: read_samples


def clear_old_outputs():
    """
    Clear any old output files from any previous runs.
    :return: void
    """
    files_to_remove = glob.glob("outputs/**/*.txt", recursive=True)

    # Delete any output files from the SOLUTIONS output directory
    for f in files_to_remove:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    # end: for-loop
# end: clear_old_outputs


if __name__ == '__main__':
    """
    The starting point to the application.
    Using the input_file defined below, solve the provided puzzles using the
    various algorithms defined in the XPuzzleSolver class.
    """
    # Print a message indicating that the application has started
    print("\nStarting X-Puzzle Solver Application")
    print("====================================\n")

    # Get the starting time of the application
    start_time = time.time()

    # Define where to read in the sample puzzles
    # *** NOTE *** Change this to point to the desired file to execute
    input_file = "inputs/sample_inputs.txt"

    # Define how many rows are supposed to be in each of the puzzles
    # *** NOTE *** Change this to the desired number of rows as needed
    number_of_rows = 2

    # Define how many seconds must pass before a search algorithm should be timed out
    # *** NOTE *** Change this value to the desired number
    algorithm_timeout = 60

    # Get the list of samples to use this run
    sample_puzzles = read_samples(input_file)

    # Clear any output files from a previous run
    clear_old_outputs()

    # Start processing our puzzles
    start(sample_puzzles, number_of_rows, algorithm_timeout)

    # Get the ending time of the application
    end_time = time.time()

    # Print the total execution time that the application took
    execution_time = end_time - start_time
    print("X-Puzzle Solver has finished... took %d seconds\n" % execution_time)
# end: __main__
