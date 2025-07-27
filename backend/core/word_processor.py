import re

class WordProcessor:

    def clean_lyrics(self, lyrics):
        lyrics = lyrics.lower()

        lyrics = re.sub(r'\[.*?\]', '', lyrics) #[]
        lyrics = re.sub(r'\(.*?\)', '', lyrics) #()
        lyrics = re.sub(r'\{.*?\}', '', lyrics) #{}
        lyrics = re.sub(r'&', 'and', lyrics) #&

        lyrics = re.sub(r'[.,?;"\'\’]', '', lyrics) #.,?;

        # apply hyphen logic
        lyrics = self.hyphens(lyrics)
        
        return lyrics
    
    def hyphens(self, text):
        '''
        Handles hyphenated words by adding a space between them.
        For example, "t-talk" becomes "talk".
        If the hyphen is the only thing after a letter, it will be left alone.
        '''

        if re.search(r'[a-zA-Z]-[a-zA-Z]', text):
            text = re.sub(r'([a-zA-Z])-([a-zA-Z])', r'\1 \2', text)
        
        return text
    
    def multipliers(self, lyrics):
        '''
        
        '''

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