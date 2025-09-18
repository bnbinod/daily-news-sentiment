import pandas as pd
import re
import aiohttp
import asyncio


class SentimentAnalyzer:
    def __init__(self):
        self.lm_positive = None
        self.lm_negative = None
        self.initialized = False

    async def initialize(self):
        """Initialize LM dictionaries asynchronously"""
        if self.initialized:
            return

        async with aiohttp.ClientSession() as session:
            # Load positive words
            async with session.get(
                    "https://raw.githubusercontent.com/okcredit/loughran-mcdonald/master/positive.csv") as resp:
                pos_data = await resp.text()
                self.lm_positive = set(pd.read_csv(pd.compat.StringIO(pos_data))['word'].str.lower().tolist())

            # Load negative words
            async with session.get(
                    "https://raw.githubusercontent.com/okcredit/loughran-mcdonald/master/negative.csv") as resp:
                neg_data = await resp.text()
                self.lm_negative = set(pd.read_csv(pd.compat.StringIO(neg_data))['word'].str.lower().tolist())

        self.initialized = True

    def preprocess(self, text):
        """Clean and tokenize text"""
        if not text or pd.isna(text):
            return []
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text.split()

    def calculate_sentiment(self, text):
        """Calculate LM sentiment scores"""
        tokens = self.preprocess(text)
        if not tokens:
            return 0, 0, 0

        pos = sum(1 for word in tokens if word in self.lm_positive)
        neg = sum(1 for word in tokens if word in self.lm_negative)
        total = len(tokens)
        net_score = (pos - neg) / total if total > 0 else 0

        return pos, neg, net_score

    def analyze_article(self, title, summary):
        """Analyze both title and summary"""
        title_pos, title_neg, title_score = self.calculate_sentiment(title)
        summary_pos, summary_neg, summary_score = self.calculate_sentiment(summary)

        return {
            'title_score': title_score,
            'summary_score': summary_score,
            'title_positive': title_pos,
            'title_negative': title_neg,
            'summary_positive': summary_pos,
            'summary_negative': summary_neg
        }


# Global analyzer instance
analyzer = SentimentAnalyzer()