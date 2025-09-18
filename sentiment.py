import pandas as pd
import re
import aiohttp
import asyncio


class SentimentAnalyzer:
    def __init__(self):
        self.lm_positive = None
        self.lm_negative = None
        self.initialized = False

    def initialize(self):
        """Initialize LM dictionaries from local CSV file"""
        if self.initialized:
            return

        try:
            # Load the local CSV file
            lm_df = pd.read_csv('instance/LM-SA-2020.csv')

            # Filter for positive and negative words
            positive_words = lm_df[lm_df['sentiment'] == 'Positive']['word'].str.lower().tolist()
            negative_words = lm_df[lm_df['sentiment'] == 'Negative']['word'].str.lower().tolist()

            # Convert to sets for faster lookup
            self.lm_positive = set(positive_words)
            self.lm_negative = set(negative_words)

            self.initialized = True
            print(f"Loaded {len(self.lm_positive)} positive words and {len(self.lm_negative)} negative words")

        except FileNotFoundError:
            print("Error: LM-SA-2020.csv file not found. Please ensure the file is in the same directory.")
            raise
        except Exception as e:
            print(f"Error loading sentiment dictionary: {e}")
            raise

    def preprocess(self, text):
        """Clean and tokenize text"""
        if not text or pd.isna(text):
            return []
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation, keep letters and spaces
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