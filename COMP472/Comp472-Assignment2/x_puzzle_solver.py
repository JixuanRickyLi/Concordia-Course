from threading import Thread
import time
from algorithms.greedy_best_first_search import GreedyBestFirstSearch
from algorithms.a_star import AStar
from algorithms.uniform import UniformCost


class XPuzzleSolver:
    """
    Used to run the various algorithms to solve one or more sample puzzle configurations.
    Will loop through each provided initial-state of the X-puzzle and attempt the solve it
    using: uniform-cost, greedy-best-first-search, and a* (GBFS and A* will use two different heuristics).
    The output of each algorithm will be written within the 'outputs' directory.
    """

    def __init__(self, puzzles_as_strings, number_of_rows_per_puzzle, algorithm_timeout):
        """
        Initialize the xPuzzleSolver class with the list of initial-states to try and solve.
        :param puzzles_as_strings: The list of puzzles to solve (array of strings representing the initial-states).
        :param number_of_rows_per_puzzle: The number of rows for every puzzle.
        :param algorithm_timeout: The max number of seconds that each algorithm has until it must be timed out.
        """
        # We should convert the array of strings of the initial-states into arrays to be used in our algorithms
        puzzles_as_arrays = []
        for puzzle in puzzles_as_strings:
            # Split each puzzle configuration by the separator (which is a space character)
            puzzles_as_arrays.append(puzzle.split(" "))
        # end: for-loop

        # Set the local variables
        self.puzzles = puzzles_as_arrays
        self.number_of_rows = number_of_rows_per_puzzle
        self.algorithm_timeout = algorithm_timeout
    # end: __init__

    def solve(self):
        """
        Will run each algorithm against every provided input puzzle in an attempt to solve it.
        :return: void
        """
        # To keep track of the puzzle number being solved
        puzzle_number = 0

        # To keep track of all of our threads
        threads = []

        # Loop through every puzzle
        for puzzle in self.puzzles:
            # Print a message saying we are starting to process this puzzle
            print("-> Starting puzzle #%d..." % puzzle_number, flush=True)
            start_time = time.time()

            # Clear the threads array so we can start fresh for this puzzle
            threads.clear()

            # Create one instance of every search algorithm to be used on the puzzle
            ucs_algo = UniformCost(puzzle_number, puzzle, self.number_of_rows, self.algorithm_timeout)
            gbfs_h1_algo = GreedyBestFirstSearch(puzzle_number, puzzle, 1, self.number_of_rows, self.algorithm_timeout)
            gbfs_h2_algo = GreedyBestFirstSearch(puzzle_number, puzzle, 2, self.number_of_rows, self.algorithm_timeout)
            astar_h1_algo = AStar(puzzle_number, puzzle, 1, self.number_of_rows, self.algorithm_timeout)
            astar_h2_algo = AStar(puzzle_number, puzzle, 2, self.number_of_rows, self.algorithm_timeout)

            # Create the thread definition for each of the search algorithms
            usc_thread = Thread(target=ucs_algo.solve)
            gbfs_h1_thread = Thread(target=gbfs_h1_algo.solve)
            gbfs_h2_thread = Thread(target=gbfs_h2_algo.solve)
            astar_h1_thread = Thread(target=astar_h1_algo.solve)
            astar_h2_thread = Thread(target=astar_h2_algo.solve)

            # Add the thread to the list so we can join them all back later
            threads.append(usc_thread)
            threads.append(gbfs_h1_thread)
            threads.append(gbfs_h2_thread)
            threads.append(astar_h1_thread)
            threads.append(astar_h2_thread)

            # Start the execution of each of the threads
            usc_thread.start()
            gbfs_h1_thread.start()
            gbfs_h2_thread.start()
            astar_h1_thread.start()
            astar_h2_thread.start()

            # Loop through each of the execution threads and join them back
            for thread in threads:
                thread.join()
            # end: for-loop

            # Print a message saying we are done processing this puzzle
            end_time = time.time()
            execution_time = end_time - start_time
            print("-> Done puzzle #%d (took %d seconds)\n" % (puzzle_number, execution_time), flush=True)

            # Don't forget to increment the puzzle number at the end of the loop
            puzzle_number += 1
        # end: for-loop
    # end: solve
# end: class XPuzzleSolver
