import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# === CONFIG ===
GNEWS_API_KEY = "5a057fbc085dd87985b068336a96375e"  # Replace with your actual key
GNEWS_API_URL = "https://gnews.io/api/v4/search"

# === PAGE SETUP ===
st.set_page_config(page_title="President News Dashboard", layout="wide")
st.title("📰 President News Dashboard")

# === FILE UPLOAD ===
st.sidebar.header("Upload President List")
uploaded_file = st.sidebar.file_uploader("Upload a CSV with Institution, Title, First, Last", type=["csv"])

sample_data = pd.DataFrame({
    "Institution": ["American University", "Amherst College", "Augsburg University"],
    "Title": ["President", "President", "President"],
    "First": ["Jon", "Michael", "Paul"],
    "Last": ["Alger", "Elliott", "Pribbenow"]
})

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8', encoding_errors='replace')
else:
    st.sidebar.info("Using sample data — upload a CSV to replace it.")
    df = sample_data

# === SEARCH FUNCTION ===
def fetch_news(first, last, institution):
    query = f'"{institution}" AND president AND ("{first} {last}" OR "{last}")'
    params = {
        "q": query,
        "token": GNEWS_API_KEY,
        "lang": "en",
        "country": "us",
        "max": 5
    }
    try:
        response = requests.get(GNEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        return []

# === DISPLAY PRESIDENTS ===
st.subheader("Presidents with Recent News")
has_news = []
no_news = []

for _, row in df.iterrows():
    first = row["First"]
    last = row["Last"]
    institution = row["Institution"]
    news = fetch_news(first, last, institution)
    if news:
        has_news.append((row, news))
    else:
        no_news.append((row, []))

# Show presidents with news — 3 per row
for i in range(0, len(has_news), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(has_news):
            row, articles = has_news[i + j]
            with cols[j]:
                st.markdown(f"### 🟢 {row['First']} {row['Last']}<br><small>{row['Institution']}</small>", unsafe_allow_html=True)
                for article in articles:
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.markdown(f"<small>📅 {article['publishedAt'][:10]} &nbsp;&nbsp; 🗞 {article['source']['name']}</small>", unsafe_allow_html=True)
                    st.markdown("---")

# Show presidents with NO news — grayed out
if no_news:
    st.subheader("Presidents with No Recent News")
    for i in range(0, len(no_news), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(no_news):
                row, _ = no_news[i + j]
                with cols[j]:
                    st.markdown(f"<div style='color: gray;'>⚪ {row['First']} {row['Last']}<br><small>{row['Institution']}</small><br><em>No recent news found</em></div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("Created with ❤️ using Streamlit + GNews.io")
