'''

Handles syllable operations for the application.

Sylabble operations include:
    - lyrics cleaning (removing punctuation, brackets, etc.)
    - lyrics normalization (lowercase)
    - lyrics correction (e.g. replacing stuttered lyrics with a single word)
    - multiplies lyrics by a factor provided by the lyircs (e.g. (x2) for doubling the lyrics)
    - conversion to syllables

Example usage:

    parameter: "
            [Intro]
            You're just jealous
            Jealous? Jealous?
            You don't even e—

            [Verse 1]
            Unseen forces, they been spreading me thin
            P-post it, pawning off dreams that you had
           "

    return: "
            youre just jea lous
            jea lous jea lous
            you dont even 

            un seen for ces they been spread ing me thin
            post it pawn ing off dreams that you had
           "

'''
import re
import pyphen

class SyllableProcessor:

    def syllables(self, lyrics):

        lyrics = self.preprocess_lyrics(lyrics)

        dic = pyphen.Pyphen(lang='en')
        words = lyrics.split()
        syllabified = [dic.inserted(word, '-') for word in words]
        lyrics = ' '.join(syllabified).replace('-', ' ')

        return lyrics

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

        
    
    def preprocess_lyrics(self, lyrics):

        lyrics = self.multipliers(lyrics)
        lyrics = self.clean_lyrics(lyrics)

        return lyrics