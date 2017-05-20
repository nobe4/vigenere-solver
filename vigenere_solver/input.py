import sys
import os


def get_key():
    """Wait for the next key pressed and return its ascii code."""
    result = None

    if os.name == 'nt':  # Windows
        import msvcrt
        result = msvcrt.getch()
    else:               # Linux
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return ord(result)
