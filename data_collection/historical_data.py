import yfinance as yf
import pandas as pd
import psycopg2
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import POSTGRES_CONFIG

# Detailed runtime information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_historical_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical market data for a given ticker using yfinance.
    :param ticker: Yahoo Finance ticker symbol (e.g., "EURUSD=X")
    :param start_date: Start date for historical data (YYYY-MM-DD)
    :param end_date: End date for historical data (YYYY-MM-DD)
    :return: DataFrame containing historical market data.
    """
    logging.info(f"Fetching historical data for {ticker} from {start_date} to {end_date}")
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    logging.info(f"Retrieved {len(data)} rows of data")
    return data

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data by resetting the index, normalizing column names,
    and removing the ticker suffix from columns.
    :param data: Raw DataFrame from yfinance.
    :return: Preprocessed DataFrame.
    """
    # Reset the index so the date becomes a column.
    data.reset_index(inplace=True)

    # Helper function: flatten column names and replace spaces with underscores.
    def flatten_col(col):
        if isinstance(col, tuple):
            return '_'.join(x.strip().replace(" ", "_") for x in col).strip().lower()
        else:
            return str(col).strip().replace(" ", "_").lower()

    # Flatten all columns.
    data.columns = [flatten_col(col) for col in data.columns]

    # If the date column was flattened to 'date_', rename it to 'date'
    if 'date_' in data.columns:
        data.rename(columns={'date_': 'date'}, inplace=True)

    # Remove ticker suffix from columns.
    # Example: if columns are like "open_eurusd=x", we want "open"
    suffix = None
    for col in data.columns:
        if col != 'date' and '_' in col:
            parts = col.rsplit('_', 1)
            if len(parts) == 2:
                suffix = f"_{parts[1]}"
                break

    if suffix:
        new_cols = {}
        for col in data.columns:
            if col != 'date' and col.endswith(suffix):
                new_cols[col] = col[:-len(suffix)]
            else:
                new_cols[col] = col
        data.rename(columns=new_cols, inplace=True)

    logging.info("Data preprocessing complete; columns normalized")
    return data

def store_historical_data(data: pd.DataFrame) -> None:
    """
    Store the preprocessed historical data in a PostgreSQL database.
    :param data: Preprocessed DataFrame.
    """

    # Establish connection using parameters from config
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()
        logging.info("Connected to PostgreSQL databases successfully")
    except Exception as e:
        logging.error("Failed to connect to PostgreSQL", exc_info=True)
        return

    # Create the table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS historical_data (
        date DATE PRIMARY KEY,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        adj_close FLOAT,
        volume BIGINT
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    logging.info("Ensured that table 'historical_data' exists")

    # Insert data row by row with an upsert mechanism (ON CONFLICT DO NOTHING)
    for _, row in data.iterrows():
        insert_query = """
        INSERT INTO historical_data (date, open, high, low, close , adj_close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING;
        """
        cur.execute(insert_query, (
            row['date'],
            row['open'],
            row['high'],
            row['low'],
            row['close'],
            row.get('adj_close', row['close']), # Fallback to 'close'
            row['volume']
        ))
    conn.commit()
    logging.info("Historical data inserted successfully into PostgreSQL")

    cur.close()
    conn.close()

if __name__ == "__main__":
    # Example usage: fetching and storing EUR/USD historical data for 2023
    ticker = "EURUSD=X"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    raw_data = fetch_historical_data(ticker, start_date, end_date)
    processed_data = preprocess_data(raw_data)
    print("Processed Columns:", processed_data.columns)
    store_historical_data(processed_data)