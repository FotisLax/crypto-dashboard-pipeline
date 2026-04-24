import requests
import psycopg2
import time

DB_CONFIG = {
    "host": "postgres",   # VERY IMPORTANT
    "database": "crypto_db",
    "user": "postgres",
    "password": "132"
}

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
    return response.json()


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

    conn.commit()
    cursor.close()
    conn.close()


while True:
    try:
        print("Fetching data...")
        data = fetch_data()
        insert_data(data)
        print("Updated successfully!")
    except Exception as e:
        print("Error:", e)

    time.sleep(15)