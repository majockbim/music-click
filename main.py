'''
    Main entry point for the Music Click application.

    Now supports both manual lyrics input and Genius URL scraping.
'''
import sys

from backend.core.text_processor import TextProcessor
from backend.utilities.enhanced_input import EnhancedLyricsInput

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
    print("\n" + "=" * 40)
    print("CHOOSE PROCESSING MODE")
    print("=" * 40)
    print("1. Syllable Mode (click for each syllable)")
    print("2. Word Mode (click for each word)")
    choice = input("Enter the number of your choice: ")
    while choice not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Enter the number of your choice: ")
    return choice

def main():
    print("MUSIC CLICK - LYRICS PROCESSOR")
    print("Supports manual input and Genius URL scraping")
    
    # Get lyrics using enhanced input system  
    lyrics_input = EnhancedLyricsInput()
    lyrics = lyrics_input.lyrics_input()
    
    # process lyrics
    processor = TextProcessor()
    
    mode = choose_mode()
    if mode == '1':
        text = processor.process_syllables(lyrics)
        print("\n" + "=" * 50)
        print("SYLLABLE MODE ACTIVE")
        print("=" * 50)
        print("Press SPACE to see the next syllable")
        print("Press 'q' to quit")
        print("Press Ctrl+C to exit")
    elif mode == '2':
        text = processor.process_words(lyrics)
        print("\n" + "=" * 50)
        print("WORD MODE ACTIVE") 
        print("=" * 50)
        print("Press SPACE to see the next word")
        print("Press 'q' to quit")
        print("Press Ctrl+C to exit")

    text_parts = text.split()
    total_parts = len(text_parts)
    
    print(f"\nReady! {total_parts} {'syllables' if mode == '1' else 'words'} loaded.")
    print("\nPress any key to start...")
    get_key()  # wait for user to be ready
    
    i = 0
    while i < len(text_parts):
        try:
            key = get_key()

            if key == ' ':
                print(f"[{i+1}/{total_parts}] {text_parts[i]}")
                i += 1
                
                # show completion message
                if i >= len(text_parts):
                    print("\n" + "=" * 30)
                    print("🎵 SONG COMPLETE! 🎵")
                    print("=" * 30)
                    break
                    
            elif key == 'q':
                print(f"\nExited at position {i+1}/{total_parts}")
                break
            elif key == '\x03':  # Ctrl+C
                print(f"\nInterrupted at position {i+1}/{total_parts}")
                break
            else:
                # ignore other keys, but could add more controls here
                pass
                
        except KeyboardInterrupt:
            print(f"\nInterrupted at position {i+1}/{total_parts}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    print("\nThank you for using Music Click!")

if __name__ == "__main__":
    main()