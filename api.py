from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import pandas as pd

app= Flask(__name__)
CORS(app)

def get_data():
    conn=psycopg2.connect(
        host="postgres",
        database="crypto_db",
        user="postgres",
        password="132",
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


@app.route("/crypto")
def crypto():
    data = get_data()
    return jsonify(data)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)