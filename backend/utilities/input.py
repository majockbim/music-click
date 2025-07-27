# Handles input operations for the application.

import sys

class LyricsInput:

    def lyrics_input(self):
        print("Please input song lyrics (Ctrl+Z -> Enter): ")

        # for multi line input
        lyrics = sys.stdin.read()
        return lyrics