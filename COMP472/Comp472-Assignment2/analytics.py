def read_search_file(ser_file):
    """
    Read the contents of the search file.
    :param ser_file: The solution file.
    :return: The file's length_of_search_file.
    """
    num_lines = 0

    while True:
        # Get the next line from the file
        line = ser_file.readline()

        # If the line is empty, we are done reading
        if not line:
            break

        num_lines += 1
    # end: while

    return num_lines
# end: read_search_file


def read_solution_file(sol_file):
    """
    Read the contents of the solution file.
    :param sol_file: The solution file.
    :return: The file's length_of_solution_path, num_no_solutions, cost_of_solution, execution_time.
    """
    num_no_solutions = 0
    num_lines = 0
    cost = 0
    time = 0.0

    while True:
        # Get the next line from the file
        line = sol_file.readline()

        # If the line is empty, we are done reading
        if not line:
            break

        # Check if this line contains "no solution"
        if "no solution" in line:
            num_no_solutions += 1

        # Else, check if this line, split by a space, contains more than 2 elements
        else:
            line_elements = line.split(" ")
            if len(line_elements) > 2:
                num_lines += 1
            else:
                cost = int(line_elements[0])
                time = float(line_elements[1])
        # end: if-else
    # end: while

    # If the file did not find a solution, the time should be set to the timeout, which is 60 seconds
    if num_no_solutions > 0:
        time = 60.0

    return num_lines, num_no_solutions, cost, time
# end: read_line


def process_data(algo, data):
    """
    Process the algorithm data.
    :param algo: The algorithm name.
    :param data: The data.
    :return:
    """
    total_solutions_found = 0
    total_ser_length = 0
    total_sol_length = 0
    total_no_solutions = 0
    total_cost = 0
    avg_costs = 0.0
    total_time = 0.0

    for d in data:
        total_sol_length += d[0][0]
        total_no_solutions += d[0][1]
        total_cost += d[0][2]
        total_time += d[0][3]
        total_ser_length += d[1][0]

        # Count all of the actual solutions,
        # for each solution found, add it's cost
        if d[0][1] == 0:
            total_solutions_found += 1
            avg_costs += d[0][2] / d[0][0]
        # end: if
    # end: for-loop

    avg_ser_length = total_ser_length / total_solutions_found
    avg_sol_length = total_sol_length / total_solutions_found
    avg_no_solutions = total_no_solutions / len(data)
    avg_cost = avg_costs / total_solutions_found
    avg_time = total_time / len(data)

    print(algo, " Average solution length: %f, Total solution length: %d" % (avg_sol_length, total_sol_length))
    print(algo, " Average no solutions: %f, Total no solutions: %d" % (avg_no_solutions, total_no_solutions))
    print(algo, " Average search length: %f, Total search length: %d" % (avg_ser_length, total_ser_length))
    print(algo, " Average cost: %f, Total cost: %d" % (avg_cost, total_cost))
    print(algo, " Average time: %f, Total time: %f" % (avg_time, total_time))
# end: process_data


if __name__ == '__main__':
    """
    This file is used just to compile the data from the resulting output files.
    """
    arr_ucs = []
    arr_gbfs_1 = []
    arr_gbfs_2 = []
    arr_astar_1 = []
    arr_astar_2 = []

    for i in range(50):
        # ****** PROCESS THE UNIFORM COST ALGORITHM DATA ******
        ucs_data = [(0, 0, 0, 0), 0]
        # Read the solution file for the ucs algorithm
        filename = "outputs/solutions/" + repr(i) + "_ucs_solution.txt"
        file = open(filename, "r")
        ucs_data[0] = read_solution_file(file)
        file.close()

        # Read the search file for the ucs algorithm
        filename = "outputs/search/" + repr(i) + "_ucs_search.txt"
        file = open(filename, "r")
        ucs_data[1] = read_solution_file(file)
        file.close()

        # Append the ucs data to the ucs list
        arr_ucs.append(ucs_data)
        # ****** PROCESS THE UNIFORM COST ALGORITHM DATA ******

        # ****** PROCESS THE GBFS H(1) ALGORITHM DATA ******
        gbfs1_data = [(0, 0, 0, 0), 0]
        # Read the solution file for the ucs algorithm
        filename = "outputs/solutions/" + repr(i) + "_gbfs-h1_solution.txt"
        file = open(filename, "r")
        gbfs1_data[0] = read_solution_file(file)
        file.close()

        # Read the search file for the ucs algorithm
        filename = "outputs/search/" + repr(i) + "_gbfs-h1_search.txt"
        file = open(filename, "r")
        gbfs1_data[1] = read_solution_file(file)
        file.close()

        # Append the ucs data to the ucs list
        arr_gbfs_1.append(gbfs1_data)
        # ****** PROCESS THE GBFS H(1) ALGORITHM DATA ******

        # ****** PROCESS THE GBFS H(2) ALGORITHM DATA ******
        gbfs2_data = [(0, 0, 0, 0), 0]
        # Read the solution file for the ucs algorithm
        filename = "outputs/solutions/" + repr(i) + "_gbfs-h2_solution.txt"
        file = open(filename, "r")
        gbfs2_data[0] = read_solution_file(file)
        file.close()

        # Read the search file for the ucs algorithm
        filename = "outputs/search/" + repr(i) + "_gbfs-h2_search.txt"
        file = open(filename, "r")
        gbfs2_data[1] = read_solution_file(file)
        file.close()

        # Append the ucs data to the ucs list
        arr_gbfs_2.append(gbfs2_data)
        # ****** PROCESS THE GBFS H(2) ALGORITHM DATA ******

        # ****** PROCESS THE A* H(1) ALGORITHM DATA ******
        astar1_data = [(0, 0, 0, 0), 0]
        # Read the solution file for the ucs algorithm
        filename = "outputs/solutions/" + repr(i) + "_astar-h1_solution.txt"
        file = open(filename, "r")
        astar1_data[0] = read_solution_file(file)
        file.close()

        # Read the search file for the ucs algorithm
        filename = "outputs/search/" + repr(i) + "_astar-h1_search.txt"
        file = open(filename, "r")
        astar1_data[1] = read_solution_file(file)
        file.close()

        # Append the ucs data to the ucs list
        arr_astar_1.append(astar1_data)
        # ****** PROCESS THE A* H(1) ALGORITHM DATA ******

        # ****** PROCESS THE A* H(2) ALGORITHM DATA ******
        astar2_data = [(0, 0, 0, 0), 0]
        # Read the solution file for the ucs algorithm
        filename = "outputs/solutions/" + repr(i) + "_astar-h2_solution.txt"
        file = open(filename, "r")
        astar2_data[0] = read_solution_file(file)
        file.close()

        # Read the search file for the ucs algorithm
        filename = "outputs/search/" + repr(i) + "_astar-h2_search.txt"
        file = open(filename, "r")
        astar2_data[1] = read_solution_file(file)
        file.close()

        # Append the ucs data to the ucs list
        arr_astar_2.append(astar2_data)
        # ****** PROCESS THE A* H(2) ALGORITHM DATA ******
    # end: for-loop

    process_data("ucs", arr_ucs)
    process_data("gbfs-h1", arr_gbfs_1)
    process_data("gbfs-h2", arr_gbfs_2)
    process_data("astar-h1", arr_astar_1)
    process_data("astar-h2", arr_astar_2)
# end: __main__
