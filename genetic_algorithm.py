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
            if not direction.__contains__("LLL") | direction.__contains__("RRR"):
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

    print(fit_directions)
    return 0


if __name__ == '__main__':
    main()
