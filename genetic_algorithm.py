import numpy as np
import matplotlib as plt
import seaborn as sns
import sys
import random
import string


def main():
    filename = "SeaCucumberGlobin.txt"
    create_hp_model(filename)


def create_population(size):
    # Create the population of directions; F,L,and R.
    letters = "FLR"
    # stores the population of directions
    directions = []
    # initialize the population to 5 children.
    for j in range(100):
        direction = ''.join(random.choice(letters) for i in range(size))
        directions.append(direction)
    return directions


# def get_cardinal_direction(path):
#     count = 0
#
#     for letter in path:
#         if letter == "L":
#             count = count - 1
#         if letter == "R":
#             count = count + 1
#         if letter
#


def create_hp_model(filename):
    # H-Hydrophobic, F-Hydrophilic
    amino_dict = {"X": "H", "A": "H", "R": "F", "N": "F", "D": "F",
                  "C": "H", "Q": "F", "E": "F", "G": "F", "H": "F",
                  "I": "H", "L": "H", "K": "F", "M": "H", "F": "H",
                  "P": "H", "S": "F", "T": "F", "W": "H", "Y": "H", "V": "H"}
    # This shows the proteins that are hydrophobic and hydrophilic in the input sequence
    h_f_list = []

    # open and read from the fasta file
    try:
        input_file = open(filename, "r")
    except FileNotFoundError:
        print("Error: specified input file, '" + filename + "', does not exist.")
        sys.exit(1)

    raw_sequences = []
    amino_acid_sequences = []
    single_aminos = []
    # Trim the header from the input file
    for raw_sequence in input_file:
        if raw_sequence[0] != ">":
            raw_sequences.append(raw_sequence)
    # Trim the new line character from the
    for sequence in raw_sequences:
        amino_acid_sequence = sequence[0:-1]
        amino_acid_sequences.append(amino_acid_sequence)
    for polypeptide in amino_acid_sequences:
        for i in range(len(polypeptide)):
            single_aminos.append(polypeptide[i])

    sequence_length = len(single_aminos)
    print(single_aminos)
    print(sequence_length)

    # fill up the h_f_list for the input file.
    for x in single_aminos:
        amino_property = amino_dict.get(x)
        h_f_list.append(amino_property)
    print(h_f_list)

    # |--------------------CREATING THE POPULATION--------------------|
    directions = create_population(sequence_length)

    # |--------------------SELECTION--------------------|
    # 1. Evaluating fitness
    # If the direction contains LLL or FFF then we can't consider it fit
    has_kids = False
    while not has_kids:
        # This contains the fit children
        fit_directions = []
        for direction in directions:
            if not direction.__contains__("LLLL") | direction.__contains__("RRRR"):
                fit_directions.append(direction)
        # This happens if all children have bumps. In this case try making a new population until you have kids that
        # don't have bumps
        if len(fit_directions) == 0:
            has_kids = False
            directions = create_population(sequence_length)
        else:
            has_kids = True

    # At this point fit_directions contains the directions that don't cause bumps.
    # Use the directions to plot the Hydrophobic or Hydrophillic properties in a 2-D array.
    # First get the cardinal direction based off of each direction.
    count = 0
    d = "W"
    facing = []
    fd = []
    for direction in fit_directions:
        for letter in direction:
            # remove fd later
            fd.append(letter)

            if letter == "L":
                count = count - 1
            elif letter == "R":
                count = count + 1
            else:
                count = count + 0

            if count % 4 == 0:
                d = "E"
            elif count % 4 == 1:
                d = "S"
            elif count % 4 == 2:
                d = "W"
            elif count % 4 == 3:
                d = "N"
            facing.append(d)

        # At this point we have the correct cardinal directions based off of each direction we had to go in.
        # Fill out a 2D matrix that is sequence_length by sequence_length; starting from the middle;
        # in the lattice represent H(Hydrophobic) as 1 and F(Hydrophyllic) as 0
        x = int(sequence_length / 2)
        y = int(sequence_length / 2)
        lattice = [[2] * sequence_length] * sequence_length
        matrix = np.array(lattice)

        # If the sequence starts with a Hydrophobic protein insert a "1" at the center of the matrix insert "0"
        # otherwise
        if h_f_list[0] == "H":
            matrix[x][y] = 1
        else:
            matrix[x][y] = 0
        for i in range(sequence_length):
            if facing[i - 1] == "N":
                if fd[i] == "L":
                    y = y - 1
                elif fd[i] == "R":
                    y = y + 1
                elif fd[i] == "F":
                    x = x + 1

            elif facing[i - 1] == "E":
                if fd[i] == "L":
                    x = x + 1
                elif fd[i] == "R":
                    x = x - 1
                elif fd[i] == "F":
                    y = y + 1

            elif facing[i - 1] == "S":
                if fd[i] == "L":
                    y = y + 1
                elif fd[i] == "R":
                    y = y - 1
                elif fd[i] == "F":
                    x = x - 1

            elif facing[i - 1] == "W":
                if fd[i] == "L":
                    x = x - 1
                elif fd[i] == "R":
                    x = x + 1
                elif fd[i] == "F":
                    y = y - 1

            if h_f_list[i] == "H":
                matrix[x][y] = 1
            else:
                matrix[x][y] = 0







        print(fd)
        print(matrix)
    print(facing)
    return 0


if __name__ == '__main__':
    main()
