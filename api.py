from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import pandas as pd
import logging
import os

app= Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

def get_data():
    conn=psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port="5432"
    )

    query= """
    SELECT *
    FROM crypto_prices
    ORDER BY timestamp DESC
    LIMIT 50
    """

    df = pd.read_sql(query, conn)
    df = df.fillna(0)
    conn.close()

    return df.to_dict(orient ="records")


#|Routing|
@app.route("/crypto")
def crypto():
    logger.info("API request received: /crypto")

    try:
        data = get_data()
        logger.info(f"Returning {len(data)} records")
        return jsonify(data)
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)