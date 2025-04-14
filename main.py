# main.py
import json
from datetime import datetime
import os
from core.fetcher import RSSFetcher
from core.nlp import ContentAnalyzer
from core.db import ArticleDatabase

def load_config():
    with open('configs/config.json') as f:
        return json.load(f)

def generate_newsletters():
    config = load_config()
    fetcher = RSSFetcher()
    analyzer = ContentAnalyzer()
    db = ArticleDatabase()

    for user, prefs in config['user_personas'].items():
        print(f"\nProcessing {user}...")
        articles = fetcher.fetch_feeds(prefs['sources'], config['rss_feeds'])
        db.save_articles(articles)

        # Generate personalized content
        newsletter = f"# {user}'s Personalized Newsletter\n\n"
        newsletter += f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for article in articles[:5]:  # Top 5 articles
            newsletter += f"## {analyzer.highlight_keywords(article['title'], prefs['interests'])}\n"
            newsletter += f"*Source: {article['source']}*\n"
            newsletter += f"{analyzer.highlight_keywords(article['summary'], prefs['interests'])}\n"
            newsletter += f"[Read more]({article['link']})\n\n"

        # Save output
        os.makedirs("outputs", exist_ok=True)
        filename = f"outputs/{user.replace(' ', '_')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(newsletter)
        print(f"Saved newsletter to {filename}")

if __name__ == "__main__":
    generate_newsletters()