def get_state_as_string(state):
    """
    Get the state as a string.
    :param state: The state to be returned as a string.
    :return: The string representation of the state.
    """
    string_state = ""
    for element in state:
        string_state += " " + element
    return string_state.lstrip()
# end: get_state_as_string


class Helper:
    """
    Class contains some common helper functions that the search algorithms will need to use.
    Such helper functions include the different movement functions as well as the 'is_goal_state' function.
    """

    def __init__(self, size_of_puzzle, number_of_rows=2):
        """
        Initialize the helper object.
        :param size_of_puzzle: The size of the puzzle (how many cells are there in all).
        :param number_of_rows: The number of rows in the puzzle.
        """
        # Define the puzzle properties
        self.puzzle_length = size_of_puzzle
        self.number_of_rows = number_of_rows
        self.puzzle_width = int(size_of_puzzle / number_of_rows)

        # Define the costs for each of the types of moves
        regular_move_cost = 1
        wrapping_move_cost = 2
        diagonal_move_cost = 3

        # These are all of the 'regular' moves
        self.cost_of_move_up = regular_move_cost
        self.cost_of_move_down = regular_move_cost
        self.cost_of_move_right = regular_move_cost
        self.cost_of_move_left = regular_move_cost

        # These are all of the 'wrapping' moves
        self.cost_of_wrap_move = wrapping_move_cost

        # These are all of the 'diagonal' moves
        self.cost_of_diagonal_adjacent = diagonal_move_cost
        self.cost_of_diagonal_across = diagonal_move_cost
    # end: __init__

    def is_goal_state(self, current_state):
        """
        Check if the current state is one of the goal states.
        There are two goal states, defined by the assignment in section 1.1 on page 1.
        :param current_state: The current state of the puzzle.
        :return: boolean, True if the current state is in fact a goal state, False otherwise.
        """
        # Default the variable to be true
        is_goal = True

        # Check if the current state equals goal state 1
        for i in range(1, self.puzzle_length):
            if int(current_state[i - 1]) != i:
                is_goal = False
                break
        # end: for-loop

        # Only check if the current state equals goal state 2
        # if we didn't already determine it was goal state 1
        if not is_goal:
            is_goal = True  # Reset the value
            counter = 1
            # Check if the current state equals goal state 2
            for j in range(self.puzzle_width):
                for i in range(self.number_of_rows):
                    if int(current_state[i * self.puzzle_width + j]) != counter:
                        is_goal = False
                        break
                    else:
                        # Increment our counter
                        counter += 1

                        # If we reached the last element, we want to set it to 0,
                        # since that is what the last element should be in goal-state-2
                        if counter == self.puzzle_length:
                            counter = 0
                # end: inner-for-loop
            # end: outer-for-loop
        # end: if

        return is_goal
    # end: is_goal_state

    def can_move_up(self, index):
        """
        Can the current state perform the 'move up' action.
        :param index: The index of the '0' tile.
        :return: True if the current_state can perform a 'move up' action, false otherwise.
        """
        # If the index of the '0' tile is in the top-row then we cannot do the action
        if index in range(0, self.puzzle_width):
            return False
        return True
    # end: can_move_up

    def can_move_down(self, index):
        """
        Can the current state perform the 'move down' action.
        :param index: The index of the '0' tile.
        :return: True if the current_state can perform a 'move down' action, false otherwise.
        """
        # If the index of the '0' tile is in the bottom-row then we cannot do the action
        if index in range(self.puzzle_length - self.puzzle_width, self.puzzle_length):
            return False
        return True
    # end: can_move_down

    def can_move_left(self, index):
        """
        Can the current state perform the 'move left' action.
        :param index: The index of the '0' tile.
        :return: True if the current_state can perform a 'move left' action, false otherwise.
        """
        # Get all of the indices that belong to the left-most tiles
        left_most_indices = [i * self.puzzle_width for i in range(0, self.number_of_rows)]

        # If the index of the '0' tile is in any of the left-most positions, then we cannot do the action
        if index in left_most_indices:
            return False

        return True
    # end: can_move_left

    def can_move_right(self, index):
        """
        Can the current state perform the 'move right' action.
        :param index: The index of the '0' tile.
        :return: True if the current_state can perform a 'move right' action, false otherwise.
        """
        # Get all of the indices that belong to the right-most tiles
        right_most_indices = [(i * self.puzzle_width) + self.puzzle_width - 1 for i in range(0, self.number_of_rows)]

        # If the index of the '0' tile is in any of the right-most positions, then we cannot do the action
        if index in right_most_indices:
            return False

        return True
    # end: can_move_right

    def can_move_wrap(self, index):
        """
        Can the current state perform the 'wrap' action.
        :param index: The index of the '0' tile.
        :return: True if the current_state can perform a 'wrap' action, false otherwise.
        """
        # Define the indices that the '0' tile is allowed to be in for a wrapping move (all four corners)
        allowed_indices = [0, self.puzzle_width - 1, self.puzzle_length - self.puzzle_width, self.puzzle_length - 1]

        # If the index of the '0' tile is not in any of the allowed positions, then we cannot do the action
        if index not in allowed_indices:
            return False

        return True
    # end: can_move_wrap

    def can_move_diagonally(self, index):
        """
        Can the current state perform the 'diagonal' action.
        :param index: The index of the '0' tile.
        :return: True if the current_state can perform a 'diagonal' action, false otherwise.
        """
        # Define the indices that the '0' tile is allowed to be in for a diagonal move (all four corners)
        allowed_indices = [0, self.puzzle_width - 1, self.puzzle_length - self.puzzle_width, self.puzzle_length - 1]

        # If the index of the '0' tile is not in any of the allowed positions, then we cannot do the action
        if index not in allowed_indices:
            return False

        return True
    # end: can_move_diagonally

    def move_up(self, current_state):
        """
        A "regular move", which involves moving the '0' tile up one cell.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'move up' action, then exit the function
        if not self.can_move_up(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile up by one and swap it with the tile that was there
        else:
            # To find the index of the tile 'directly above' the '0', we can simply subtract the '0' index by the width
            # of the puzzle
            index_to_swap = index - self.puzzle_width

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_move_up, tile_that_was_swapped
    # end: move_up

    def move_down(self, current_state):
        """
        A "regular move", which involves moving the '0' tile down one cell.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'move down' action, then exit the function
        if not self.can_move_down(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile down by one and swap it with the tile that was there
        else:
            # To find the index of the tile 'directly below' the '0', we can simply add the '0' index by the width
            # of the puzzle
            index_to_swap = index + self.puzzle_width

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_move_down, tile_that_was_swapped
    # end: move_down

    def move_left(self, current_state):
        """
        A "regular move", which involves moving the '0' tile left one cell.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'move left' action, then exit the function
        if not self.can_move_left(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile left by one and swap it with the tile that was there
        else:
            # To find the index of the tile 'directly to the left' of the '0', we can simply subtract the '0' index by 1
            index_to_swap = index - 1

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_move_left, tile_that_was_swapped
    # end: move_left

    def move_right(self, current_state):
        """
        A "regular move", which involves moving the '0' tile right one cell.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'move right' action, then exit the function
        if not self.can_move_right(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile right by one and swap it with the tile that was there
        else:
            # To find the index of the tile 'directly to the right' of the '0', we can simply add to the '0' index by 1
            index_to_swap = index + 1

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_move_right, tile_that_was_swapped
    # end: move_right

    def wrap(self, current_state):
        """
        A "wrapping move", which involves moving the '0' tile from one of the corner positions across (horizontally)
        to the opposite tile in the same row.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'wrap' action, then exit the function
        if not self.can_move_wrap(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile to the other side of the grid
        else:
            # We need to find the opposite position of the '0' tile
            index_to_swap = index

            # If the '0' tile is in the top-left corner, then we need to switch it with the tile in the top-right corner
            if index == 0:
                index_to_swap = self.puzzle_width - 1

            # If the '0' tile is in the top-right corner, then we need to switch it with the tile in the top-left corner
            elif index == self.puzzle_width - 1:
                index_to_swap = 0

            # If the tile is in the bottom-left corner, then we need to switch with the tile in the bottom-right corner
            elif index == self.puzzle_length - self.puzzle_width:
                index_to_swap = self.puzzle_length - 1

            # If the tile is in the bottom-right corner, then we need to switch with the tile in the bottom-left corner
            elif index == self.puzzle_length - 1:
                index_to_swap = self.puzzle_length - self.puzzle_width

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_wrap_move, tile_that_was_swapped
    # end: wrap

    def wrap_scale(self, current_state):
        """
        A "wrapping move", but when the game board is scaled up, which involves moving the '0' tile from one of the
        corner positions across (vertically) to the opposite tile in the same column.
        This is only applicable when the game board has more than two rows.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'wrap' action, then exit the function
        if not self.can_move_wrap(index):
            return 0, tile_that_was_swapped

        # Check if the game board has more than 2 rows
        elif self.number_of_rows <= 2:
            return 0, tile_that_was_swapped

        # Else, we can perform the swap
        else:
            # We need to find the opposite position of the '0' tile
            index_to_swap = index

            # If the '0' tile is in the top-left corner, then we need to switch it with the bottom-left corner
            if index == 0:
                index_to_swap = self.puzzle_length - self.puzzle_width

            # If the '0' tile is in the top-right corner, then we need to switch it with the bottom-right corner
            elif index == self.puzzle_width - 1:
                index_to_swap = self.puzzle_length - 1

            # If the tile is in the bottom-left corner, then we need to switch it with the top-left corner
            elif index == self.puzzle_length - self.puzzle_width:
                index_to_swap = 0

            # If the tile is in the bottom-right corner, then we need to switch it with the top-right corner
            elif index == self.puzzle_length - 1:
                index_to_swap = self.puzzle_width - 1

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_wrap_move, tile_that_was_swapped
    # end: wrap_scale

    def diagonal_adjacent(self, current_state):
        """
        A "diagonal move", which involves moving the '0' tile from one of the corner positions to diagonally adjacent.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'diagonal' action, then exit the function
        if not self.can_move_diagonally(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile to the other side of the grid
        else:
            # We need to find the adjacent-diagonal position of the '0' tile
            index_to_swap = index

            # If the '0' tile is in the top-left corner, then we need to switch it with the tile +1 row and +1 column
            if index == 0:
                index_to_swap = index + self.puzzle_width + 1

            # If the '0' tile is in the top-right corner, then we need to switch it with the tile +1 row and -1 column
            elif index == self.puzzle_width - 1:
                index_to_swap = index + self.puzzle_width - 1

            # If the tile is in the bottom-left corner, then we need to switch with the tile -1 row and +1 column
            elif index == self.puzzle_length - self.puzzle_width:
                index_to_swap = index - self.puzzle_width + 1

            # If the tile is in the bottom-right corner, then we need to switch with the tile -1 row and -1 column
            elif index == self.puzzle_length - 1:
                index_to_swap = index - self.puzzle_width - 1

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_diagonal_adjacent, tile_that_was_swapped
    # end: diagonal_adjacent

    def diagonal_across(self, current_state):
        """
        A "diagonal move", which involves moving the '0' tile from one of the corner positions to diagonally across.
        :param current_state: The current configuration of the puzzle. NOTE: We are modifying the array by reference.
        :return: A tuple containing the cost of performing this move, and the tile that was swapped.
        """
        # Find the index of the '0' tile
        index = current_state.index('0')
        tile_that_was_swapped = '0'

        # If the current state can't perform the 'diagonal' action, then exit the function
        if not self.can_move_diagonally(index):
            return 0, tile_that_was_swapped

        # Else, we can move the '0' tile to the other side of the grid
        else:
            # We need to find the diagonal-across position of the '0' tile
            index_to_swap = index

            # If the '0' tile is in the top-left corner, then we need to switch it with the bottom-right corner
            if index == 0:
                index_to_swap = self.puzzle_length - 1

            # If the '0' tile is in the top-right corner, then we need to switch it with the bottom-left corner
            elif index == self.puzzle_width - 1:
                index_to_swap = self.puzzle_length - self.puzzle_width

            # If the '0' tile is in the bottom-left corner, then we need to switch it with the top-right corner
            elif index == self.puzzle_length - self.puzzle_width:
                index_to_swap = self.puzzle_width - 1

            # If the '0' tile is in the bottom-right corner, then we need to switch it with the top-left corner
            elif index == self.puzzle_length - 1:
                index_to_swap = 0

            # Swap the '0' tile with the other index
            tile_that_was_swapped = current_state[index_to_swap]
            current_state[index] = current_state[index_to_swap]
            current_state[index_to_swap] = '0'
        # end: if-else

        return self.cost_of_diagonal_across, tile_that_was_swapped
    # end: diagonal_across

    def generate_children(self, current_state):
        """
        Generate all of the possible children for the current state of the game.
        :param current_state: The current state of the game.
        :return: A list of tuples containing:
                   1. the modified state of that particular move,
                   2. the cost of the move,
                   3. the name of the move,
                   4. the specific tile that was moved.
        """
        # Define a list of the possible moves that this current state can make
        list_of_possible_moves = []

        # Find the index of the '0' tile
        index = current_state.index('0')

        # Check all the possible moves and see which are possible for this current state
        move_up_copy = current_state.copy()
        result = self.move_up(move_up_copy)
        if result[0] > 0:
            list_of_possible_moves.append((move_up_copy, self.cost_of_move_up, 'move_up', result[1]))

        move_down_copy = current_state.copy()
        result = self.move_down(move_down_copy)
        if result[0] > 0:
            list_of_possible_moves.append((move_down_copy, self.cost_of_move_down, 'move_down', result[1]))

        move_left_copy = current_state.copy()
        result = self.move_left(move_left_copy)
        if result[0] > 0:
            list_of_possible_moves.append((move_left_copy, self.cost_of_move_left, 'move_left', result[1]))

        move_right_copy = current_state.copy()
        result = self.move_right(move_right_copy)
        if result[0] > 0:
            list_of_possible_moves.append((move_right_copy, self.cost_of_move_right, 'move_right', result[1]))

        # Two possible moves can be done if the wrap is allowed
        if self.can_move_wrap(index):
            # The regular (horizontal) wrap
            regular_wrap_copy = current_state.copy()
            result = self.wrap(regular_wrap_copy)
            if result[0] > 0:
                list_of_possible_moves.append((regular_wrap_copy, self.cost_of_wrap_move, 'wrap', result[1]))

            # The scaled-up (vertical) wrap
            scaled_wrap_copy = current_state.copy()
            result = self.wrap_scale(scaled_wrap_copy)
            if result[0] > 0:
                list_of_possible_moves.append((scaled_wrap_copy, self.cost_of_wrap_move, 'wrap_scale', result[1]))
        # end: if

        # Two possible moves can be done if the diagonal action is allowed
        if self.can_move_diagonally(index):
            # The diagonal adjacent:
            diagonal_adjacent_copy = current_state.copy()
            result = self.diagonal_adjacent(diagonal_adjacent_copy)
            list_of_possible_moves.append(
                (diagonal_adjacent_copy, self.cost_of_diagonal_adjacent, 'diagonal_adjacent', result[1]))

            # The diagonal across:
            diagonal_across_copy = current_state.copy()
            result = self.diagonal_across(diagonal_across_copy)
            list_of_possible_moves.append(
                (diagonal_across_copy, self.cost_of_diagonal_across, 'diagonal_across', result[1]))
        # end: if

        # Return the list of possible moves
        return list_of_possible_moves
    # end: generate_children

    def get_goal_state_1(self):
        """
        Get the goal state 1 list of tokens.
        :return:
        """
        goal_state_1 = [str(i) for i in range(1, self.puzzle_length)]
        goal_state_1.append('0')
        return goal_state_1
    # end: get_goal_state_1

    def get_goal_state_2(self):
        """
        Get the goal state 2 list of tokens.
        :return:
        """
        # Create a list with the total number of elements for this puzzle
        goal_state_2 = ['0'] * self.puzzle_length

        counter = 1
        for j in range(self.puzzle_width):
            for i in range(self.number_of_rows):
                goal_state_2[i * self.puzzle_width + j] = str(counter)
                counter += 1

                # If we reached the last element, we want to set it to 0,
                # since that is what the last element should be in goal-state-2
                if counter == self.puzzle_length:
                    counter = 0
            # end: inner-for-loop
        # end: outer-for-loop

        return goal_state_2
    # end: get_goal_state_2

    def h0(self, current_state):
        """
        The "default" heuristic, defined by the assignment specifications.
        If the '0' tile is in the last index, return 0, otherwise return 1, for all states.
        :param current_state: The current state of the puzzle.
        :return: The heuristic value.
        """
        index = current_state.index('0')
        if index == self.puzzle_length - 1:
            return 0

        return 1
    # end: h0

    def continuous(self, current_state):
        """
        The function that check if current state is continuous with one exception
        ex) 12345607 or 01234567 ->True
        :return: bool if it's continuous state or not.
        """
        h = 0
        for i in range(1, self.puzzle_length):
            if int(current_state[i - 1]) == i - h:
                continue
            elif int(current_state[i - 1]) == 0:
                h = 1
            else:
                return False
        return True
    # end: connected

    def h1(self, current_state):
        """
        The first heuristic.
        This heuristic implements the "Hamming Distance" calculation.
        :param current_state: The current state of the puzzle.
        :return: The heuristic value.
        """
        # Default the variable to be true
        is_goal = True

        # Define the two heuristics for each goal state
        h_goal_1 = 0
        h_goal_2 = 0

        # Check if the current state equals goal state 1
        for i in range(1, self.puzzle_length):
            if int(current_state[i - 1]) != i:
                h_goal_1 += 1
                is_goal = False
        # end: for-loop

        # Only check for the second goal state if the current state does not equal the goal
        # and if we didn't already determine it was goal state 1
        if not is_goal:
            # Reset the value
            is_goal = True
            counter = 1

            # Check if the current state equals goal state 2
            for j in range(self.puzzle_width):
                for i in range(self.number_of_rows):
                    if int(current_state[i * self.puzzle_width + j]) != counter:
                        is_goal = False
                        h_goal_2 += 1

                        # Increment our counter
                        counter += 1

                        # If we reached the last element, we want to set it to 0,
                        # since that is what the last element should be in goal-state-2
                        if counter == self.puzzle_length:
                            counter = 0
                # end: inner-for-loop
            # end: outer-for-loop
        # end: if

        if self.continuous(current_state):
            return min(h_goal_1, h_goal_2)
        else:
            return 2 * min(h_goal_1, h_goal_2)
        # Return the minimum of the two heuristics
    # end: h1

    def h2(self, current_state):
        """
        The second heuristic.
        This heuristic implements the "Manhattan Distance" calculation.
        :param current_state: The current state of the puzzle.
        :return: The heuristic value.
        """
        # Setup these lists to be equal to the two goal states
        goal_1 = self.get_goal_state_1()
        goal_2 = self.get_goal_state_2()

        # Find the manhattan distance from the current state to the first goal state
        h_goal_1 = sum(
            abs(b % self.puzzle_width - g % self.puzzle_width) + abs(b // self.puzzle_width - g // self.puzzle_width)
            for b, g in ((current_state.index(str(i)), goal_1.index(str(i))) for i in range(self.puzzle_length))
        )

        # Find the manhattan distance from the current state to the second goal state
        h_goal_2 = sum(
            abs(b % self.puzzle_width - g % self.puzzle_width) + abs(b // self.puzzle_width - g // self.puzzle_width)
            for b, g in ((current_state.index(str(i)), goal_2.index(str(i))) for i in range(self.puzzle_length))
        )

        # Return the minimum between the two heuristic values to each goal
        return min(h_goal_1, h_goal_2)
    # end: h2
# end: class Helper
