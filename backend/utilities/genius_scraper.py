"""
Genius.com scraper for extracting song lyrics and metadata.

This scraper extracts:
- Song lyrics text
- Song title and artist
- YouTube links (if available)
- Other streaming service links

Usage:
    scraper = GeniusScraper()
    data = scraper.scrape_song("https://genius.com/song-url")
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
import json

class GeniusScraper:
    
    def __init__(self):
        self.session = requests.Session()
        # Use a realistic user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_song(self, url):
        """
        Scrape a Genius song page for lyrics and metadata.
        
        Args:
            url (str): Full Genius URL for the song
            
        Returns:
            dict: Contains lyrics, title, artist, and links
        """
        try:
            # Add delay to be respectful to the server
            time.sleep(1)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic song info
            song_data = {
                'url': url,
                'title': self._extract_title(soup),
                'artist': self._extract_artist(soup),
                'lyrics': self._extract_lyrics(soup),
                'youtube_links': self._extract_youtube_links(soup),
                'streaming_links': self._extract_streaming_links(soup)
            }
            
            return song_data
            
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None
        except Exception as e:
            print(f"Error parsing page: {e}")
            return None
    
    def _extract_title(self, soup):
        """Extract song title from the page."""
        # Try multiple selectors for title
        selectors = [
            'h1[class*="SongHeaderdesktop"]',
            '.header_with_cover_art-primary_info-title',
            'h1',
            '[data-lyrics-container] h1'
        ]
        
        for selector in selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            # Remove "Lyrics" and site name from title
            title = title_tag.get_text()
            title = re.sub(r'\s*–\s*Genius.*$', '', title)
            title = re.sub(r'\s*Lyrics\s*$', '', title)
            return title.strip()
        
        return "Unknown Title"
    
    def _extract_artist(self, soup):
        """Extract artist name from the page."""
        # Try multiple selectors for artist
        selectors = [
            'a[class*="SongHeaderdesktop__Artist"]',
            '.header_with_cover_art-primary_info-primary_artist',
            '[data-lyrics-container] a[href*="/artists/"]'
        ]
        
        for selector in selectors:
            artist_elem = soup.select_one(selector)
            if artist_elem:
                return artist_elem.get_text().strip()
        
        return "Unknown Artist"
    
    def _extract_lyrics(self, soup):
        """Extract lyrics text from the page."""
        # Look for the main lyrics container
        lyrics_containers = [
            '[data-lyrics-container="true"]',
            '.Lyrics__Container',
            '.lyrics',
            '[class*="Lyrics__Container"]'
        ]
        
        lyrics_text = ""
        
        for selector in lyrics_containers:
            containers = soup.select(selector)
            for container in containers:
                # Remove script tags and other non-lyric content
                for script in container(["script", "style"]):
                    script.decompose()
                
                # Get text and preserve line breaks
                text = container.get_text(separator='\n', strip=True)
                lyrics_text += text + '\n'
        
        if not lyrics_text.strip():
            # Fallback: look for any div that might contain lyrics
            possible_lyrics = soup.find_all('div', string=re.compile(r'\[.*?\]'))
            for elem in possible_lyrics:
                parent = elem.parent
                if parent:
                    lyrics_text += parent.get_text(separator='\n', strip=True) + '\n'
        
        return lyrics_text.strip()
    
    def _extract_youtube_links(self, soup):
        """Extract YouTube links from the page."""
        youtube_links = []
        
        # Look for YouTube links in various places
        youtube_patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+'
        ]
        
        # Check all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            for pattern in youtube_patterns:
                if re.match(pattern, href):
                    youtube_links.append(href)
        
        # Also check in script tags for embedded data
        for script in soup.find_all('script'):
            if script.string:
                for pattern in youtube_patterns:
                    matches = re.findall(pattern, script.string)
                    youtube_links.extend(matches)
        
        # Remove duplicates
        return list(set(youtube_links))
    
    def _extract_streaming_links(self, soup):
        """Extract other streaming service links."""
        streaming_links = {}
        
        # Common streaming services
        services = {
            'spotify': r'https?://open\.spotify\.com/track/[\w]+',
            'apple_music': r'https?://music\.apple\.com/.*?',
            'soundcloud': r'https?://soundcloud\.com/.*?',
            'bandcamp': r'https?://.*?\.bandcamp\.com/.*?'
        }
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            for service, pattern in services.items():
                if re.match(pattern, href):
                    if service not in streaming_links:
                        streaming_links[service] = []
                    streaming_links[service].append(href)
        
        return streaming_links
    
    def validate_genius_url(self, url):
        """Check if the URL is a valid Genius song URL."""
        parsed_url = urlparse(url)
        return (
            parsed_url.netloc in ['genius.com', 'www.genius.com'] and
            parsed_url.path and
            parsed_url.path != '/'
        )

# Example usage and testing
if __name__ == "__main__":
    scraper = GeniusScraper()
    
    # Test URL validation
    test_url = "https://genius.com/Artist-song-title-lyrics"
    
    if scraper.validate_genius_url(test_url):
        print("Valid Genius URL")
        # Uncomment to test actual scraping
        # result = scraper.scrape_song(test_url)
        # if result:
        #     print(f"Title: {result['title']}")
        #     print(f"Artist: {result['artist']}")
        #     print(f"YouTube links: {result['youtube_links']}")
        #     print(f"Lyrics preview: {result['lyrics'][:200]}...")
    else:
        print("Invalid Genius URL")