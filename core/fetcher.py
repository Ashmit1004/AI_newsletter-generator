import feedparser
from datetime import datetime
from typing import List, Dict
import logging
from bs4 import BeautifulSoup

class RSSFetcher:
    """Handles all RSS feed fetching and processing"""
    
    def __init__(self, max_articles_per_feed: int = 3):
        self.max_articles = max_articles_per_feed

    def clean_text(self, text: str) -> str:
        """Fix encoding and HTML entities"""
        if not text:
            return ""
        
        if isinstance(text, list):
            text = ' '.join([str(item) for item in text])
        
        try:
            text = str(text).encode('utf-8', errors='ignore').decode('utf-8')
        except UnicodeError:
            text = str(text).encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
        
        return BeautifulSoup(text, "html.parser").get_text().replace('\xa0', ' ').strip()

    def fetch_feeds(self, sources: List[str], rss_mapping: Dict[str, str]) -> List[Dict]:
        """Main method to fetch and process feeds"""
        articles = []
        for source in sources:
            try:
                if source in rss_mapping:
                    feed = feedparser.parse(rss_mapping[source])
                    articles.extend(self._process_feed(feed, source))
            except Exception as e:
                logging.error(f"RSS fetch failed for {source}: {e}")
        return articles

    def _process_feed(self, feed, source: str) -> List[Dict]:
        """Process individual feed entries"""
        processed = []
        for entry in feed.entries[:self.max_articles]:
            processed.append({
                'title': self.clean_text(getattr(entry, 'title', '')),
                'link': getattr(entry, 'link', ''),
                'summary': self.clean_text(getattr(entry, 'summary', '')),
                'source': source,
                'published': getattr(entry, 'published', datetime.now().isoformat()),
            })
        return processed