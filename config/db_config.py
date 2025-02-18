import os

# PostgreSQL configuration
POSTGRES_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'trading_db'),
    'user': os.getenv('POSTGRES_USER', 'db_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'db_password'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432))  # Ensure port is an integer
}

# MongoDB configuration
MONGO_CONFIG = {
    'url': os.getenv('MONGO_URL', 'mongodb://localhost:27017/'),
    'database': os.getenv('MONGO_DB', 'trading_db'),
    'collection': os.getenv('MONGO_COLLECTION', 'news_sentiment')
}
