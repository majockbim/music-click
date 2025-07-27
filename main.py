'''
    Main entry point for the Music Click application.

    Mainly used for testing at this point.
'''
import sys

from core.syllable_processor import SyllableProcessor
from core.word_processor import WordProcessor
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

def choose_mode():
    print("Choose your desired mode: ")
    print("1. Syllable Mode")
    print("2. Word Mode")
    choice = input("Enter the number of your choice: ")
    while choice not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Enter the number of your choice: ")
    return choice

def main():
    mode = choose_mode()
    if mode == '1':
        text = SyllableProcessor().syllables(LyricsInput().lyrics_input())
    elif mode == '2':
        text = WordProcessor().process(LyricsInput().lyrics_input())

    text = text.split()

    # print("You entered the following lyrics: \n")
    # print(text)

    print("Press space to see the next word, or 'q' to quit.")

    i = 0
    while i < len(text):
        key = get_key()

        if key == ' ':
            print(text[i])
            i += 1
        elif key == 'q':
            break
        elif key == '\x03': # Ctrl+C
            break

    print("Thank you for testing.")

if __name__ == "__main__":
    main()