import requests
import psycopg2
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "postgres",   # VERY IMPORTANT
    "database": "crypto_db",
    "user": "postgres",
    "password": "132"
}

def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id TEXT PRIMARY KEY,
            symbol TEXT,
            name TEXT,
            current_price FLOAT,
            market_cap BIGINT,
            volume_24h BIGINT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        logger.error(f"CoinGecko error: {response.status_code} - {response.text}")
        return []

    data = response.json()

    if not isinstance(data, list):
        logger.error(f"Unexpected API response: {data}")
        return []

    return data

#|Data insertion|
def insert_data(coins):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for coin in coins:
        cursor.execute("""
            INSERT INTO crypto_prices 
            (id, symbol, name, current_price, market_cap, volume_24h)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                current_price = EXCLUDED.current_price,
                market_cap = EXCLUDED.market_cap,
                volume_24h = EXCLUDED.volume_24h;
        """, (
            coin["id"],
            coin["symbol"],
            coin["name"],
            coin["current_price"],
            int(coin["market_cap"]),
            int(coin["total_volume"])
        ))
    if not coins:
        logger.warning("No data received, skipping insert.")
        return

    conn.commit()
    cursor.close()
    conn.close()

create_table()

while True:
    try:
        logger.info("Fetching crypto data from CoinGecko...")
        data = fetch_data()
        insert_data(data)
        logger.info(f"Successfully fetched {len(data)} coins")
    except Exception as e:
        logger.error(f"Error while fetching data: {e}")

    time.sleep(60)