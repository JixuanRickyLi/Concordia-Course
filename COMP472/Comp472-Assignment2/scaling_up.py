import os
import glob
import time
import random

from algorithms.a_star import AStar


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


def generate_random_puzzle(width, height):
    """
    Generate a random puzzle with the provided dimensions.
    :param width: The width of the puzzle.
    :param height: The height of the puzzle.
    :return: The random puzzle.
    """
    # Start with all the numbers available (numbers need to be set as strings)
    number_list = [x for x in range(width * height)]

    # Start our puzzle out as an empty string and we will append each random number to it
    random_puzzle = []

    # Loop while there are will elements in the number list
    while len(number_list) > 0:
        # Pick a random number from the list
        random_number = random.choice(number_list)

        # Get the index of that random choice
        index = number_list.index(random_number)

        # Pop that element from the list
        random_number = number_list.pop(index)

        # Append the random choice to the puzzle followed by a space character
        random_puzzle.append(str(random_number))
    # end: while-loop

    return random_puzzle
# end: generate_random_puzzle


if __name__ == '__main__':
    """
    Using the best performing algorithm, we will conduct more tests on it using scaled-up versions
    of the X-puzzle.
    """
    # Clear the old run outputs
    clear_old_outputs()

    # We will perform 10 different tests on increasing puzzle sizes
    NUMBER_OF_TESTS = 10

    # Se the timeout time to 1 hour
    TIMEOUT = 3600

    # We will start off the tests on the standard 4x2 board
    width_of_puzzle = 2
    number_of_rows = 2
    increment_width = True
    increment_height = False

    # Perform all of the tests
    for i in range(NUMBER_OF_TESTS):
        # Get the starting time of this run
        print("Starting puzzle #%d, size: %dx%d... " % (i, width_of_puzzle, number_of_rows))
        start_time = time.time()

        # Generate a random puzzle with the current size
        puzzle = generate_random_puzzle(width_of_puzzle, number_of_rows)

        # Run the algorithm on the puzzle
        astar = AStar(i, puzzle, 2, number_of_rows, TIMEOUT)
        astar.solve()

        # Increment the puzzle size (every second puzzle, increment the number of rows)
        if increment_width:
            width_of_puzzle += 1
            increment_width = False
            increment_height = True
        elif increment_height:
            number_of_rows += 1
            increment_height = False
            increment_width = True
        # end: if-else

        # Get the ending time of this run
        end_time = time.time()
        execution_time = end_time - start_time
        print("Done! (took %d seconds)\n" % execution_time)
    # end: for-loop
# end: __main__
