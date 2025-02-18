from pymongo import MongoClient
import datetime
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import MONGO_CONFIG

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def store_news_sentiment(source: str, headline: str, sentiment_score: float, timestamp=None) -> None:
    """
    Store a news sentiment record in MongoDB.
    :param source: The source of the news (e.g., Twitter, Google News)
    :param headline: The headline or brief description of the news event
    :param sentiment_score: Sentiment polarity score
    :param timestamp: Time of the sentiment analysis (defaults to current UTC time)
    """
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()

    try:
        client = MongoClient(MONGO_CONFIG['url'])
        db = client[MONGO_CONFIG['database']]
        collection = db[MONGO_CONFIG['collection']]
        logging.info("Connected to MongoDB successfully")
    except Exception as e:
        logging.error("Failed to connect to MongoDB", exc_info=True)
        return

    # Create the news sentiment record
    news_record = {
        "source": source,
        "headline": headline,
        "sentiment_score": sentiment_score,
        "timestamp": timestamp
    }

    collection.insert_one(news_record)
    logging.info("News sentiment record inserted successfully")
    client.close()

if __name__ == "__main__":
    # Example usage
    store_news_sentiment(
        source="Twitter",
        headline="Market rallies as EUR/USD nears 1.10",
        sentiment_score=0.75
    )