#!/usr/bin/env python

"""
Calculates the index of coincidence (IC) for different key lengths of
a given input string, to discover the key length most likely used for
a ciphertext.
"""

import sys
import re
from collections import Counter
from argparse import ArgumentParser, FileType

# Standard index of coincidence for English.
ENGLISH_IC = 0.0667


def read_file(infile):
    """
    Reads an input file and removes any whitespace characters
    and makes all characters uppercase.
    """

    cipher_text = infile.read()

    regex = re.compile('[^a-zA-Z]')
    converted = regex.sub('', cipher_text).upper()

    return converted


def calculate_ic(text):
    """
    Calculates the IC for a given string.

    @source https://gist.github.com/enigmaticape/4254054
    """

    cipher_len = len(text)

    freqs = Counter(text)
    alphabet = map(chr, range(ord('A'), ord('Z') + 1))
    freqsum = 0.0

    for letter in alphabet:
        freqsum += freqs[letter] * (freqs[letter] - 1)

    return freqsum / (cipher_len * (cipher_len - 1))


def find_key_length(ciphertext, verbose=0):
    """
    Finds the most likely key length for the input string, using the IC method.
    Assumes that the input ciphertext is in English, with an IC of 0.0667.
    """

    closest_key_length = 0
    closest_key_delta = 100000000
    closest_key_ic = 0

    # Try key sizes up to 26, or the length of the ciphertext.
    key_size_range = range(1, min(27, len(ciphertext)))

    # Enumerates all key sizes
    for k in key_size_range:
        if verbose >= 1:
            print("Trying key size {0}...".format(k))

        # Prepare k columns.
        columns = []

        for i in range(k):
            columns.append([])

        # Arrange letters into k columns.
        for i, char in enumerate(ciphertext):
            columns[i % k].append(char)

        # Calculate IC sum.
        ic_sum = 0
        columns_calculated = 0

        # Get IC for each column.
        for i in range(k):
            column_wise = ''.join(columns[i])

            # Skip if the text is less than 2 characters.
            if len(column_wise) < 2:
                continue

            columns_calculated += 1
            index_coincidence = calculate_ic(column_wise)
            ic_sum += index_coincidence

            if verbose >= 2:
                print("Column {0}: IC={2} | {1}".format(
                    i + 1, column_wise, index_coincidence))

        # Calculate the aggregate delta IC.
        aggregate_ic = ic_sum / columns_calculated

        if verbose >= 1:
            print("Aggregate IC: {0}".format(aggregate_ic))

        # Finds if the aggregate delta IC is lesser than the previously found min delta.
        delta = abs(aggregate_ic - ENGLISH_IC)

        if delta < closest_key_delta:
            closest_key_delta = delta
            closest_key_length = k
            closest_key_ic = aggregate_ic

        if verbose >= 1:
            print()

    # Print the most likely key length.
    print("Most likely key length: {0} (or any factors of {0})".format(
        closest_key_length))
    print("Index of coincidence: {0}".format(closest_key_ic))


def main():
    """
    Prepares and parses arguments before running the script.
    """

    description = "Calculates the index of coincidence (IC) for different key lengths \
    of a given ciphertext, and finds the most probably key length based on the typical \
    English IC of 0.0667."

    # Prepare arguments.
    parser = ArgumentParser(description=description)
    parser.add_argument('-v', '--verbose', action='count',
                        help='set verbosity level', default=0)
    parser.add_argument('infile', default=sys.stdin,
                        type=FileType('r'), help='Input file to read')

    # Parse arguments.
    args = parser.parse_args()

    # Reads the file and removes all whitespaces and non-alphabetic characters.
    input_text = read_file(args.infile)

    if args.verbose >= 3:
        print("Input string: {0}".format(input_text))

    # Runs the function.
    find_key_length(input_text, verbose=args.verbose)


if __name__ == "__main__":
    main()
