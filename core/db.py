import sqlite3
from typing import List, Dict
from datetime import datetime

class ArticleDatabase:
    def __init__(self, db_path: str = "newsletter.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            source TEXT,
            published DATE,
            processed BOOLEAN DEFAULT 0
        )""")

    def save_articles(self, articles: List[Dict]):
        """Deduplicates and stores new articles"""
        for article in articles:
            try:
                self.conn.execute(
                    """INSERT OR IGNORE INTO articles 
                    VALUES (?,?,?,?,?,?)""",
                    (article['link'], article['title'], article['link'],
                     article['source'], article['published'], False)
                )
            except sqlite3.Error as e:
                print(f"DB error: {e}")
        self.conn.commit()