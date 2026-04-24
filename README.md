# 🚀 Crypto Dashboard Pipeline

A fully containerized crypto data pipeline using:

- CoinGecko API
- PostgreSQL
- Flask API
- Docker
- Chrome Extension frontend

---

## 🏗 Architecture

CoinGecko API  
→ Fetcher (every 15s)  
→ PostgreSQL  
→ Flask REST API  
→ Chrome Extension UI  

---

## 🐳 Run with Docker

### 1️⃣ Clone repository

git clone https://github.com/YOUR_USERNAME/cryptopipeline.git
cd cryptopipeline

### 2️⃣ Start everything

docker compose up --build

### 3️⃣ Open API

http://localhost:5000/crypto

---

## 🧩 Load Chrome Extension

1. Open Chrome
2. Go to chrome://extensions
3. Enable Developer Mode
4. Click "Load unpacked"
5. Select the `extension` folder

---

## ⚙️ Tech Stack

- Python
- Flask
- PostgreSQL
- Docker
- JavaScript
- Chrome Extensions API

---

## 📌 Features

- Auto-refresh every 15 seconds
- Containerized architecture
- Real-time crypto prices
- Modern UI popup