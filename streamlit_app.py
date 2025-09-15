import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# === CONFIG ===
GNEWS_API_KEY = "5a057fbc085dd87985b068336a96375e"  # Replace with your actual key
GNEWS_API_URL = "https://gnews.io/api/v4/search"

# === PAGE SETUP ===
st.set_page_config(page_title="President News Dashboard", layout="wide")
st.title("📰 Coalition President News Dashboard")

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
    df = pd.read_csv(uploaded_file, encoding='utf-8', errors='replace')
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

# === LAYOUT FUNCTION ===
def display_president_card(president, news_items):
    first = president["First"]
    last = president["Last"]
    institution = president["Institution"]

    if news_items:
        st.markdown(f"#### 🟢 {first} {last}")
        st.markdown(f"**{institution}**")
        for article in news_items:
            title = article.get("title", "Untitled")
            link = article.get("url", "")
            source = article.get("source", {}).get("name", "Unknown Source")
            date_str = article.get("publishedAt", "")
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                date_str = date_obj.strftime("%b %d, %Y")
            except:
                pass
            st.markdown(f"- [{title}]({link})  ")
            st.markdown(f"🗞 {source} | 📅 {date_str}")
    else:
        st.markdown(f"#### ⚪ {first} {last}")
        st.markdown(f"**{institution}**")
        st.markdown(f"<span style='color:gray;'>(No recent news found)</span>", unsafe_allow_html=True)

# === DISPLAY PRESIDENTS ===
with_news = []
without_news = []

for _, row in df.iterrows():
    news = fetch_news(row["First"], row["Last"], row["Institution"])
    if news:
        with_news.append((row, news))
    else:
        without_news.append((row, []))

st.markdown("### 🟢 Presidents with News")
for i in range(0, len(with_news), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(with_news):
            with
