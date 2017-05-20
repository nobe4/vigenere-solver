import re


def read_file(filename):
    """Read and prepare the content of the file."""
    with open(filename) as f:
        # Read the whole file
        return f.read()


def filter_content(content):
    """Apply a filter on the content, to clear the text and keep only
    letters."""

    # Keep only letters, and lowercase them
    return re.sub('[^a-zA-Z]+', '', content).lower()


def generate_key(shifts):
    """Generate the vigenere key from the shifts."""
    return "".join(map(lambda x: chr(ord('z') - x + 1), shifts))


def generate_shifts(key):
    """Generate the vigenere shifts from the key."""
    return list(map(lambda x:  ord('z') - ord(x) + 1, key))


def decode_message(string, shifts):
    """Decode the message, shifting only letters in the string."""

    result = ""

    # Because not all characters are shifted, keep track here of the current
    # shift index.
    current_shift = 0

    for char in string:
        current_char = char
        reference = None

        # Check if the current character is a letter, and depending on the
        # case, save the current character reference.
        if 'a' <= current_char <= 'z':
            reference = ord('a')
        elif 'A' <= current_char <= 'Z':
            reference = ord('A')

        # If the character is a letter, the reference exists and we need to
        # shift the value.
        if reference:
            result += chr(
                reference +
                (
                    ord(current_char)
                    - reference
                    + shifts[current_shift % len(shifts)]
                ) % 26
            )
            current_shift += 1
        # Otherwise, save the current char
        else:
            result += current_char

    return result
