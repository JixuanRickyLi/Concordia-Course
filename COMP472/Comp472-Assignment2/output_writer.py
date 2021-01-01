class OutputWriter:
    """
    This class is responsible for writing to the output files for a particular algorithm and heuristic.
    For example, the SOLUTION output for the first "Greedy Best First Search" algorithm, using heuristic 1,
    should output to the following path: "outputs/solutions/0_gbfs-h1_solution.txt".
    """

    def __init__(self, puzzle_num, algorithm, heuristic='0'):
        """
        Initialize this OutputWriter object.
        Set the path to use for writing as well as the specific heuristic being used.
        :param puzzle_num The puzzle number being processed.
        :param algorithm: The algorithm key being processed (i.e. ucs, gbfs, astar).
        :param heuristic: The heuristic function being used (i.e. 0, 1, 2).
        """
        # Set the path to the output file using the algorithm and heuristic
        self.solution_output = "outputs/solutions/" + repr(puzzle_num) + "_" + algorithm
        self.search_output = "outputs/search/" + repr(puzzle_num) + "_" + algorithm

        # If the heuristic is non-zero, then we should add that to the output file path
        if heuristic != '0':
            self.solution_output += "-h" + repr(heuristic)
            self.search_output += "-h" + repr(heuristic)
        # end: if

        self.solution_output += "_solution.txt"
        self.search_output += "_search.txt"
    # end: __init__

    def write_line_to_solution(self, line_to_write):
        """
        Writes the provided line to the solution output file.
        :param line_to_write: The line to be written in the solution output file.
        :return: void
        """
        # Create the file connection, append the line, and close the file connection
        f = open(self.solution_output, "a")
        f.write(line_to_write + "\n")
        f.close()
    # end: writeLineToSolution

    def write_line_to_search(self, line_to_write):
        """
        Writes the provided line to the search output file.
        :param line_to_write: The line to be written in the search output file.
        :return: void
        """
        # Create the file connection, append the line, and close the file connection
        f = open(self.search_output, "a")
        f.write(line_to_write + "\n")
        f.close()
    # end: writeLineToSolution
# end: class OutputWriter
