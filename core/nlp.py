import re
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ContentAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def highlight_keywords(self, text: str, keywords: List[str]) -> str:
        """Adds **bold** markdown to keywords"""
        for kw in filter(None, keywords):
            text = re.sub(fr'\b({re.escape(kw)})\b', r'**\1**', text, flags=re.IGNORECASE)
        return text

    def calculate_relevance(self, text: str, interests: List[str]) -> float:
        """Semantic similarity score (0-1)"""
        if not text or not interests:
            return 0.0
        text_embed = self.model.encode([text])
        interest_embeds = self.model.encode(interests)
        return float(np.max(cosine_similarity(text_embed, interest_embeds)))