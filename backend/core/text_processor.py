'''
Main text processor that handles both syllable and word processing.

This class serves as the main interface for processing lyrics, handling
common preprocessing steps and delegating to specialized processors.

'''
import re
import pyphen

class TextProcessor:
    
    def __init__(self):
        self.dic = pyphen.Pyphen(lang='en')
    
    def process_syllables(self, lyrics):
        """
        Process lyrics and return syllable-separated text.
        """
        lyrics = self._preprocess_lyrics(lyrics)
        words = lyrics.split()
        syllabified = [self.dic.inserted(word, '-') for word in words]
        lyrics = ' '.join(syllabified).replace('-', ' ')
        return lyrics
    
    def process_words(self, lyrics):
        """
        Process lyrics and return word-separated text.
        """
        lyrics = self._preprocess_lyrics(lyrics)
        return lyrics
    
    def _preprocess_lyrics(self, lyrics):
        """
        Common preprocessing steps for both syllable and word processing.
        """
        lyrics = self._handle_multipliers(lyrics)
        lyrics = self._clean_lyrics(lyrics)
        return lyrics
    
    def _clean_lyrics(self, lyrics):
        """
        Clean and normalize lyrics text.
        """
        lyrics = lyrics.lower()

        # Remove brackets and parentheses content
        lyrics = re.sub(r'\[.*?\]', '', lyrics)  # []
        lyrics = re.sub(r'\(.*?\)', '', lyrics)  # ()
        lyrics = re.sub(r'\{.*?\}', '', lyrics)  # {}
        
        # Replace ampersand
        lyrics = re.sub(r'&', 'and', lyrics)
        
        # Remove punctuation
        lyrics = re.sub(r'[.,?;"\'\']', '', lyrics)
        
        # Handle hyphens
        lyrics = self._handle_hyphens(lyrics)
        
        return lyrics
    
    def _handle_hyphens(self, text):
        """
        Handles hyphenated words by adding a space between them.
        For example, "t-talk" becomes "t talk".
        If the hyphen is the only thing after a letter, it will be left alone.
        """
        if re.search(r'[a-zA-Z]-[a-zA-Z]', text):
            text = re.sub(r'([a-zA-Z])-([a-zA-Z])', r'\1 \2', text)
        
        return text
    
    def _handle_multipliers(self, lyrics):
        """
        Handle multiplier patterns like (x2), (x3), (2x), (3x), etc.
        Repeats the line the specified number of times.
        """
        lines = lyrics.split('\n')
        processed_lines = []
        
        for line in lines:
            # Check for multiplier patterns: (x2), (x3), (2x), (3x), etc.
            multiplier_match = re.search(r'\((?:x(\d+)|(\d+)x)\)', line)
            
            if multiplier_match:
                # Extract the multiplier number
                multiplier = int(multiplier_match.group(1) or multiplier_match.group(2))
                
                # Remove the multiplier from the line
                base_line = re.sub(r'\s*\((?:x\d+|\d+x)\)', '', line).strip()
                
                # Repeat the line
                for _ in range(multiplier):
                    processed_lines.append(base_line)
            else:
                # No multiplier found, keep the line as is
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)