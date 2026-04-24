import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# -----------------------
# DB CONNECTION
# -----------------------
conn = psycopg2.connect(
    host="localhost",
    database="crypto_db",
    user="postgres",
    password="132",
    port="5432"
)

# -----------------------
# LOAD DATA
# -----------------------
query = """
SELECT *
FROM crypto_prices
ORDER BY timestamp DESC
LIMIT 500
"""

df = pd.read_sql(query, conn)

# -----------------------
# UI TITLE
# -----------------------
st.title("📊 Crypto Dashboard")

# -----------------------
# SHOW TABLE
# -----------------------
st.subheader("Latest Data")
st.dataframe(df.head(50))

# -----------------------
# PRICE LINE CHART
# -----------------------
st.subheader("Price Over Time")

fig = px.line(
    df,
    x="timestamp",
    y="price_usd",
    color="coin_id",
    title="Crypto Prices"
)

st.plotly_chart(fig)

# -----------------------
# PIE CHART (Market Cap)
# -----------------------
st.subheader("Market Cap Distribution")

latest = df.sort_values("timestamp").groupby("coin_id").last().reset_index()

fig2 = px.pie(
    latest.head(10),
    names="coin_id",
    values="market_cap",
    title="Top 10 Market Cap"
)

st.plotly_chart(fig2)

# -----------------------
# BAR CHART (Volume)
# -----------------------
st.subheader("Trading Volume")

fig3 = px.bar(
    latest.head(10),
    x="coin_id",
    y="volume_24h",
    title="Top 10 Volume"
)

st.plotly_chart(fig3)