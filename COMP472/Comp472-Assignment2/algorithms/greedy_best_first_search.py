import time
import numpy as np

from output_writer import OutputWriter
from algorithms.node import Node
from algorithms.helper import Helper
from algorithms.helper import get_state_as_string


class GreedyBestFirstSearch:
    """
    This class is responsible for executing the "greedy-best-first-search" search algorithm on the
    provided puzzle instance.
    """

    def __init__(self, puzzle_num, puzzle, heuristic_number, number_of_rows_per_puzzle, timeout):
        """
        Initialize this search algorithm object.
        :param puzzle_num: The puzzle number this is currently solving.
        :param puzzle: The initial-state of the puzzle.
        :param heuristic_number: The heuristic function to use (i.e. 1, or 2).
        :param number_of_rows_per_puzzle: The number of rows that each puzzle will contain.
        :param timeout: The max number of seconds this algorithm has until it must be timed out.
        """
        # Set the puzzle's initial state
        self.puzzle = puzzle
        self.heuristic = heuristic_number

        # Set the timeout time (in seconds)
        self.timeout = timeout

        # Set the helper class for use in solving the search
        self.helper = Helper(len(puzzle), number_of_rows_per_puzzle)

        # Define the output writer for this algorithm
        self.output_writer = OutputWriter(puzzle_num, "gbfs", heuristic_number)
        self.open_list = [Node(puzzle, None, 0, None, 0, None)]
        self.closed_list = []
    # end: __init__

    def solve(self):
        """
        Solve the puzzle using the greedy best first search search algorithm.
        :return: void
        """
        print("   Starting gbfs-h%d..." % self.heuristic, flush=True, end="\n")

        # We want to continue to loop until we have reached one of the following conditions:
        #   1. There are no more nodes in the open list (no solution found)
        #   2. We have reached the goal state (solution found)
        #   3. We have exceeded the timeout limit (no solution found)
        found_goal = False
        goal_node = None
        start_time = time.time()
        execution_time = 0

        while len(self.open_list) > 0 and execution_time < self.timeout:
            # Step 1: Extract the first element from the open_list (since it's sorted)
            #         Also ensure that element is removed the list since we are currently visiting it
            current_node = self.open_list.pop(0)

            # Step 2: Add the current node to the closed list
            self.closed_list.append(current_node)

            # Step 3: Check if the current node is the goal
            if self.helper.is_goal_state(current_node.state):
                found_goal = True
                goal_node = current_node
                break
            # end: if

            # Step 4: Generate the children of the current node
            child_states = self.helper.generate_children(current_node.state)

            # Step 5: Calculate the total cost to reach each of the children from the root
            #         and add them into the open list if that state does not appear in the closed list
            #         and that particular state does not already exist in the open list with a lower cost
            self.handle_children(current_node, child_states)

            # Step 6: Sort the open-list by the smallest costing nodes
            self.sort_open_list()

            # For logging, write the visited node in the search file
            self.write_search(current_node)

            # Don't forget to update the time
            execution_time = time.time() - start_time
        # end: while-loop

        # Did we find a goal state?
        timedout = False
        if found_goal:
            self.write_solution(goal_node, execution_time)
        else:
            # If the solution could not be found due to a timeout
            if execution_time >= self.timeout:
                self.output_writer.write_line_to_solution("no solution (timed out)")
                timedout = True
            else:
                self.output_writer.write_line_to_solution("no solution")
            # end: if-else
        # end: if-else

        line = "   Done"
        if timedout:
            line = "   Timed-out"

        line += " gbfs-h%d!  (took " + "{:.4f}".format(execution_time) + " seconds)"
        print(line % self.heuristic, flush=True, end="\n")
    # end: solve

    def write_search(self, node):
        """
        Write a line in the search file for the current node.
        :param node: The node currently being processed.
        :return: void
        """
        # The line should contain the f(n), g(n), and h(n) followed by the state of the node
        # For GBFS, there is no f(n) so we will put 0
        h = node.heuristic_value
        g = node.cost
        f = 0

        # Write the line to the file
        self.output_writer.write_line_to_search(
            repr(f) + " " + repr(g) + " " + repr(h) + " " + get_state_as_string(node.state)
        )
    # end: write_search

    def write_solution(self, goal_node, execution_time):
        """
        Write the solution path to the output file.
        :param goal_node: The node containing the reached goal state.
        :param execution_time: The total time it took to execute the search.
        :return: void
        """
        # The first line in the solution should contain "0 0" followed by the initial puzzle state
        self.output_writer.write_line_to_solution("0 0 " + get_state_as_string(self.puzzle))

        # Set the goal node first
        lines_to_write = [
            goal_node.moved_tile + " " + repr(goal_node.move_cost) + " " + get_state_as_string(goal_node.state)
        ]

        # We will now traverse the solution path in reverse order (from goal to start), so we will store the lines to
        # write to the output file in this array and the reverse it before writing them to the output file in the
        # correct order
        current_node = goal_node
        while True:
            # Get the parent of the current node
            current_node = current_node.parent_node

            # We don't want to include the start node
            if current_node.parent_node is None:
                break

            # Write the tile that was moved, then the cost to move there, and then the state configuration
            lines_to_write.append(
                current_node.moved_tile + " " +
                repr(current_node.move_cost) + " " +
                get_state_as_string(current_node.state)
            )
        # end: while

        # Reverse the list
        lines_to_write.reverse()

        # Write each line to the output file
        for line in lines_to_write:
            self.output_writer.write_line_to_solution(line)
        # end: for-loop

        # The last line in the file should contain the total cost of the solution as well as the total execution time
        self.output_writer.write_line_to_solution(repr(goal_node.cost) + " " + "{:.4f}".format(execution_time))
    # end: write_solution

    def sort_open_list(self):
        """
        Sort the open list by the h(n) of each of the nodes.
        :return: void
        """
        self.open_list.sort(key=lambda node: node.heuristic_value)
    # end: sort_open_list

    def handle_children(self, current_node, child_states):
        """
        Handle the children generated from the current node.
        They may or may not need to be added to the open-list based on their state and cost.
        :param current_node: The node currently being processed.
        :param child_states: The list of children of the the current node.
        :return: void
        """
        # Check each of the children to see if they must be added to the open list
        for child in child_states:
            # Create the child node objects for each of the heuristics
            # GBFS does not use the f(n) or g(n) values
            # The first heuristic
            cost = current_node.cost + child[1]
            if self.heuristic == 1:
                h_1 = self.helper.h1(child[0])
                child_node = Node(child[0], current_node, cost, child[2], child[1], child[3], h_1, 0)

            # The second heuristic
            elif self.heuristic == 2:
                h_2 = self.helper.h2(child[0])
                child_node = Node(child[0], current_node, cost, child[2], child[1], child[3], h_2, 0)

            # The "default" heuristic
            else:
                h_0 = self.helper.h0(child[0])
                child_node = Node(child[0], current_node, cost, child[2], child[1], child[3], h_0, 0)
            # end: if-else

            # Check if the child state already exists in the closed list
            found_in_closed_list = False
            for node in self.closed_list:
                comparison = np.array(node.state) == np.array(child_node.state)
                if comparison.all():
                    found_in_closed_list = True
                    break
                # end: if
            # end: for-loop

            # If the node is NOT in the closed list and was NOT in the open list, we can add it to our open list
            if not found_in_closed_list:
                self.open_list.append(child_node)
        # end: for-loop
    # end: handle_children
# end: class GreedyBestFirstSearch
