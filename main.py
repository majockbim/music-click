'''
    Main entry point for the Music Click application.

    Mainly used for testing at this point.
'''
import sys

from core.syllable_processor import SyllableProcessor
from utilities.input import LyricsInput

try:
    import msvcrt  # Windows
    def get_key():
        return msvcrt.getch().decode('utf-8')
except ImportError:
    import termios, tty  # Unix/Linux/Mac
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

def main():
    text = SyllableProcessor().syllables(LyricsInput().lyrics_input())

    syllables = text.split()

    # print("You entered the following lyrics: \n")
    # print(text)

    print("Press space to see the next syllable, or 'q' to quit.")

    i = 0
    while i < len(syllables):
        key = get_key()

        if key == ' ':
            print(syllables[i])
            i += 1
        elif key == 'q':
            break
        elif key == '\x03': # Ctrl+C
            break

    print("Thank you for testing.")

if __name__ == "__main__":
    main()