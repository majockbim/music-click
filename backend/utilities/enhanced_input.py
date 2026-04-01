"""
Enhanced input handler that supports both manual lyrics input and Genius URL scraping.

This module handles:
- Manual lyrics input (original functionality)
- Genius URL validation and scraping
- Automatic lyrics extraction and processing
"""

from .genius_scraper import GeniusScraper
import re

class EnhancedLyricsInput:
    
    def __init__(self):
        self.scraper = GeniusScraper()
    
    def lyrics_input(self):
        """
        get lyrics either through manual input or Genius URL scraping.
        
        Returns:
            str: Raw lyrics text ready for processing
        """
        print("=" * 50)
        print("MUSIC CLICK - LYRICS INPUT")
        print("=" * 50)
        print("Choose input method:")
        print("1. Paste lyrics manually")
        print("2. Enter Genius URL")
        print()
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        while choice not in ['1', '2']:
            print("Invalid choice. Please enter 1 or 2.")
            choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            return self._manual_input()
        else:
            return self._genius_input()
    
    def _manual_input(self):
        """Handle manual lyrics input."""
        print("\n" + "=" * 30)
        print("MANUAL LYRICS INPUT")
        print("=" * 30)
        print("Paste your lyrics below.")
        print("Press Enter twice when finished.")
        print()
        
        lyrics_lines = []
        empty_line_count = 0
        
        while True:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
                lyrics_lines.append(line)
            else:
                empty_line_count = 0
                lyrics_lines.append(line)
        
        lyrics = '\n'.join(lyrics_lines).strip()
        
        if not lyrics:
            print("No lyrics entered. Please try again.")
            return self.lyrics_input()
        
        print(f"\nLyrics captured! ({len(lyrics.split())} words)")
        return lyrics
    
    def _genius_input(self):
        """Handle Genius URL input and scraping."""
        print("\n" + "=" * 30)
        print("GENIUS URL INPUT")
        print("=" * 30)
        print("Enter the full Genius URL for the song:")
        print("Example: https://genius.com/Artist-song-title-lyrics")
        print()
        
        url = input("Genius URL: ").strip()
        
        # Validate URL
        if not self.scraper.validate_genius_url(url):
            print("Invalid Genius URL. Please enter a valid Genius song URL.")
            return self._genius_input()
        
        print("\nScraping lyrics from Genius...")
        print("This may take a few seconds...")
        
        # Scrape the song data
        song_data = self.scraper.scrape_song(url)
        
        if not song_data:
            print("Failed to scrape lyrics from the provided URL.")
            print("Please check the URL and try again, or use manual input.")
            return self.lyrics_input()
        
        if not song_data['lyrics']:
            print("No lyrics found on this page.")
            print("Please try a different URL or use manual input.")
            return self.lyrics_input()
        
        # Display extracted information
        print("\n" + "=" * 40)
        print("EXTRACTION SUCCESSFUL!")
        print("=" * 40)
        print(f"Title: {song_data['title']}")
        print(f"Artist: {song_data['artist']}")
        
        if song_data['youtube_links']:
            print(f"YouTube links found: {len(song_data['youtube_links'])}")
            for i, link in enumerate(song_data['youtube_links'][:3], 1):  # Show first 3
                print(f"  {i}. {link}")
        
        if song_data['streaming_links']:
            print("Other streaming links found:")
            for service, links in song_data['streaming_links'].items():
                print(f"  {service.title()}: {len(links)} link(s)")
        
        lyrics_word_count = len(song_data['lyrics'].split())
        print(f"\nLyrics extracted! ({lyrics_word_count} words)")
        
        # Option to preview lyrics
        preview = input("\nWould you like to preview the lyrics? (y/n): ").strip().lower()
        if preview in ['y', 'yes']:
            print("\n" + "=" * 30)
            print("LYRICS PREVIEW (First 300 characters)")
            print("=" * 30)
            preview_text = song_data['lyrics'][:300]
            if len(song_data['lyrics']) > 300:
                preview_text += "..."
            print(preview_text)
            print("=" * 30)
        
        return song_data['lyrics']
    
    def get_song_metadata(self, url):
        """
        Get just the metadata (title, artist, links) without lyrics.
        Useful for getting additional song information.
        
        Args:
            url (str): Genius URL
            
        Returns:
            dict: Song metadata or None if failed
        """
        if not self.scraper.validate_genius_url(url):
            return None
        
        song_data = self.scraper.scrape_song(url)
        if song_data:
            # Return metadata without lyrics
            return {
                'title': song_data['title'],
                'artist': song_data['artist'],
                'youtube_links': song_data['youtube_links'],
                'streaming_links': song_data['streaming_links'],
                'url': song_data['url']
            }
        return None

# For backward compatibility
class LyricsInput(EnhancedLyricsInput):
    """Alias for backward compatibility with existing code."""
    pass