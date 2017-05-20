from collections import Counter
from string import ascii_lowercase
from vigenere_solver.input import get_key


def transpose_block(string, length):
    '''Create blocks of letter, following the given length, and transpose those blocks.'''

    # Split the string into X blocks of defined length
    blocks = [
        string[x: x + length]
        for x in range(0, len(string) - length + 1, length)
    ]

    # Transpose the blocks
    # ref: http://stackoverflow.com/a/4937526/2558252
    # In python 3, the zip return an iterator, convert to a list.
    return list(zip(*blocks))


def letter_frequencies(letters):
    '''Count the letter frequencies in an array, return a dictionnary of
    corresponding frequencies for each letters.'''

    # Count the number of letters
    counts = Counter(letters)

    frequencies = [
        # Normalize the percentage and multiply it by 100
        int(
            100 *
            float(counts.get(x, 0) * 100)
            / len(ascii_lowercase)
        )
        for x in ascii_lowercase
    ]

    return frequencies


def print_decoded_sample(string, shifts, current_blocks):
    """Print a decoded sample of the string, following the found shifts."""

    print('[D] Extract of the decoded text, v represent the current column changed.')

    shift_len = len(shifts)
    string_result = ""

    # Print indication of the current shifted block
    print(
        "\t" + "".join(
            "v" if index == current_blocks else " "
            for index in range(shift_len)
        )
    )

    # Print 5 lines of X blocks
    for index in range(shift_len * 5):
        current_shift = shifts[index % shift_len]
        # Prepare the strings, with the current shift
        string_result += chr(
            ord('a') +
            (
                ord(string[index])
                - ord('a')
                + current_shift
            ) % 26
        )

    # Print the lines
    print(
        "\t" + "\n\t".join(
            string_result[x:x + shift_len]
            for x in range(0, shift_len * 5, shift_len)
        )
    )


def print_frequencies(frequencies, frequencies_name):
    '''Print a simple chart representing the frequencies, will use 15 steps.'''

    print('[D] Frequencies for {}.'.format(frequencies_name))
    limits = range(100, 15000, 1000)

    # Print all letters
    print(' '.join(ascii_lowercase))

    # Print the chart
    for limit in limits:
        print(' '.join(
            [' ', '#'][frequence > limit]
            for frequence in frequencies
        )
        )


def shift_array(frequencies, shift):
    '''Shift an array.'''
    return frequencies[-shift:] + frequencies[:-shift]


def find_shifts(blocks, content, reference_frequencies):
    '''Interactive prompt to find the best shifts for each blocks.
    Ask the user to manually shift the blocks to make the letter frequencies match visually.
    '''

    shifts = [0] * len(blocks)

    current_block = 0
    current_shift = 0

    while current_block < len(blocks):

        print('\n---\n')

        # Shift if the current shift is set
        if current_shift:
            shifts[current_block] = (
                shifts[current_block] + current_shift) % 26
            frequencies = shift_array(frequencies, current_shift)
        # Otherwise it's a block change, update the frequencies
        # this is also the first step to be executed
        else:
            frequencies = letter_frequencies(blocks[current_block])
            # Shift the frequencies to get back to the next step
            frequencies = shift_array(frequencies, shifts[current_block])

        # Print both frequencies and the decoded sample.
        print_frequencies(reference_frequencies, 'Reference')
        print_frequencies(frequencies, 'Current')
        print_decoded_sample(content, shifts, current_block)

        # Print usage
        print('[?] Use [wasd] or [hjkl] to update the shifts.\n >  ', end='')

        # Get the pressed key
        key = get_key()

        # Reset the shift operation
        current_shift = 0

        # Shift right for d and l
        if key in [ord('d'), ord('l')]:
            current_shift = 1
        # Shift left for a and h
        elif key in [ord('a'), ord('h')]:
            current_shift = -1
        # Previous block for w, k
        elif key in [ord('w'), ord('k')]:
            current_block -= 1
            if current_block < 0:
                current_block = 0
        # Next block for every other key
        else:
            current_block += 1

    print('')
    return shifts
