import operator


def find_distances(string, sequence_lengths=(3, 7)):
    '''Get all distances between the repeating sequences in the string.
    The provided sequence_lengths define the lower and upper length to search.'''

    # Result array
    distances = []

    # For defined sequence lengths, find the repetitions and the distances
    for sequence_length in range(*sequence_lengths):

        # Hold the arrays of distances between repetitions
        repetitions = {}

        # Hold the last index for a sequence, won't be used after this function
        last_indexes = {}

        # Iterate for all chars to for a sequence, cutting at defined length
        for x in range(len(string) - (sequence_length - 1)):
            sequence = string[x:x + sequence_length]

            # Init or update the repetitions and last indexes
            if sequence not in repetitions:
                # If it's the first time the sequence is found, the distance is
                # the current position from the start of the string.
                repetitions[sequence] = [x]
            else:
                # Otherwise, take the last found index and the current position
                # difference.
                repetitions[sequence].append(x - last_indexes[sequence])

            # Update the last index found
            last_indexes[sequence] = x

        # Add only elements that are repeated at least 3 times
        for _, found_distances in repetitions.items():
            if len(found_distances) > 2:
                for distance in found_distances:
                    distances.append(distance)

    return distances


def find_key_length(distances, max_length=20):
    '''Find the numbers that divides the distance the most.'''

    # Save the divisors in a dict
    divisors = {x: 0 for x in range(max_length)}

    # For each possible divisor
    for divisor in divisors:
        # And for each found distance
        for distance in distances:
            # Keep only found divisor larger than 3.
            if divisor > 3 and distance % divisor == 0:
                divisors[divisor] += 1

    # Convert to a list of tuples
    best_divisors = [(k, v) for k, v in divisors.items()]

    # Get the  5 best divisors, one of them is the key length
    best_divisors = sorted(
        best_divisors, key=operator.itemgetter(1), reverse=True)[0:5]

    return best_divisors
