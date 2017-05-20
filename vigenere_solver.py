#!/usr/bin/env python3
'''

Vigenere Solver

Vigenere solver based on frequency analysis and manual shift selection.

Usage:
    vigenere_solver FILE
    vigenere_solver FILE [--min-sequence=MIN_SEQUENCE] [--max-sequence=MAX_SEQUENCE] [--max-length=MAX_LENGTH]
    vigenere_solver FILE --key-length=KEY_LENGTH
    vigenere_solver FILE --key=KEY
    vigenere_solver (-h | --help | -v | --version)

Examples:
    vigenere_solver example.txt
    -> Will run everything, with the default values.

    vigenere_solver example.txt --key-length=7
    -> Will run only the shift detection part, for a key length of 7.

    vigenere_solver example.txt --key='python'
    -> Will decode the file, with the key 'python'

Options:
    FILE                            The input file to read.
    --min-sequence=MIN_SEQUENCE     Specify the minimal sequence to search for. [default: 3]
    --max-sequence=MAX_SEQUENCE     Specify the maximal sequence to search for. [default: 7]
    --max-length=MAX_LENGTH         Specify the maximal length for the key. [default: 20]
    --key-length=KEY_LENGTH         If you already know the length of the key, you can set it,
                                    this will bypass all the key-length detection.
    --key=KEY                       If you already know the key, you can decode the text directly.

License:
    MIT: See LICENSE
'''
from docopt import docopt
from os.path import isfile
from sys import exit

from vigenere_solver.frequencies import find_distances, find_key_length
from vigenere_solver.shifts import transpose_block, find_shifts
from vigenere_solver.text import read_file, decode_message, filter_content, generate_key, generate_shifts

# Values for a, b, c, ... in the english language.
english_frequencies = [8167, 1492, 2782, 4253, 12702, 2228, 2015, 6094, 6966,
                       153, 772, 4025, 2406, 6749, 7507, 1929, 95, 5987, 6327, 9056, 2758,
                       978, 2360, 150, 1974, 74]

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0')

    print('[ Vigenere solver, by nobe4. ]')

    filename = arguments.get('FILE')

    if not isfile(filename):
        exit('/!\ {} does not exist.')

    print('[D] Reading from {}...'.format(filename))
    content = read_file(filename)

    filtered_content = filter_content(content)
    print('[D] Read {} bytes, {} after filtering.'.format(
        len(content), len(filtered_content)))

    key = arguments.get('--key')

    if not key:

        key_length = arguments.get('--key-length')

        if not key_length:
            min_sequence = int(arguments.get('--min-sequence'))
            max_sequence = int(arguments.get('--max-sequence'))
            print('[D] Finding distances for sequences of length between {} and {}...'.format(
                min_sequence, max_sequence))
            distances = find_distances(
                filtered_content, (min_sequence, max_sequence))

            max_length = int(arguments.get('--max-length'))
            print('[D] Found {} distances, now computing the divisors below {}...'.format(
                len(distances), max_length))

            possible_key_lengths = find_key_length(distances, max_length)
            print('[I] Best possible key length found (length, score):\n    {}'.format(
                possible_key_lengths))

            key_length = input(
                '[?] Which key length do you want to continue the analysis with?\n >  ')

        key_length = int(key_length)
        print('[D] Continuing with the key length: {}.'.format(key_length))

        blocks = transpose_block(filtered_content, key_length)
        print('[D] Transposed the content to {} blocks of length {}.'.format(
            len(blocks), len(blocks[0])))

        shifts = find_shifts(blocks, filtered_content, english_frequencies)
        key = generate_key(shifts)

        print('[D] Found shifts {}, which corresponds to the key {}.'.format(
            shifts, key))
    else:
        shifts = generate_shifts(key)

    print('[D] Decoding with key \'{}\''.format(key))

    clear_message = decode_message(content, shifts)
    print('[V] Decoded message:\n\n{}'.format(clear_message))
