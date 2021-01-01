import random

if __name__ == '__main__':
    """
    Simply generate a list of 50 random input puzzles and store them in a file.
    """
    # Define the input file name to be used for the 50 random puzzles
    filename = "inputs/fifty_random_puzzles.txt"

    # Define a list to store our 50 random puzzles
    puzzles = []

    # Loop 50 times to generate 50 random puzzles
    for i in range(50):
        # Start with all the numbers available
        number_list = [0, 1, 2, 3, 4, 5, 6, 7]

        # Start our puzzle out as an empty string and we will append each random number to it
        puzzle = ""

        # Loop while there are will elements in the number list
        while len(number_list) > 0:
            # Pick a random number from the list
            random_number = random.choice(number_list)

            # Get the index of that random choice
            index = number_list.index(random_number)

            # Pop that element from the list
            random_number = number_list.pop(index)

            # Append the random choice to the puzzle followed by a space character
            puzzle += repr(random_number) + " "
        # end: while-loop

        # Append the trimmed puzzle to the list of puzzles
        puzzles.append(puzzle.rstrip())
    # end: for-loop

    # Open the file for writing (will clear any previous data in the file)
    f = open(filename, "w")

    # Write each puzzle to the file, one puzzle per line
    for puzzle in puzzles:
        f.write(puzzle + "\n")
    # end: for-loop

    # Close the file connection
    f.close()
# end: __main__
