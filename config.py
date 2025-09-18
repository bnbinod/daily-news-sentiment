import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sentiment.db")

    # News API (get free key from https://newsapi.org/)
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_SOURCES = "bloomberg,reuters,financial-post,the-wall-street-journal"

    # Alpha Vantage for stock context (optional)
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

    # Analysis parameters
    UPDATE_INTERVAL_HOURS = 6  # Update every 6 hours