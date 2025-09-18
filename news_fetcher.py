import requests
from datetime import datetime, timedelta
from app import db, SentimentRecord
from sentiment import analyzer


class NewsFetcher:
    def __init__(self):
        self.api_key = "your_newsapi_key"  # Replace with your key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, query="finance OR economy OR stocks OR market", days=1):
        """Fetch news from NewsAPI"""
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        params = {
            'q': query,
            'sources': 'bloomberg,reuters',
            'from': from_date,
            'sortBy': 'publishedAt',
            'apiKey': self.api_key,
            'language': 'en',
            'pageSize': 50
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get('articles', [])
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return []

    def process_news(self):
        """Fetch, analyze, and store news"""
        articles = self.fetch_news()
        processed_count = 0

        for article in articles:
            # Check if article already exists
            existing = SentimentRecord.query.filter_by(url=article['url']).first()
            if existing:
                continue

            # Analyze sentiment
            sentiment = analyzer.analyze_article(
                article['title'],
                article.get('description', '') or article.get('content', '')
            )

            # Store in database
            record = SentimentRecord(
                title=article['title'][:500],  # Truncate if too long
                summary=article.get('description', '') or article.get('content', ''),
                source=article['source']['name'],
                url=article['url'],
                **sentiment
            )

            db.session.add(record)
            processed_count += 1

        db.session.commit()
        return processed_count