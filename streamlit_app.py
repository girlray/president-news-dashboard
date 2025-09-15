import streamlit as st
import pandas as pd
import requests
import urllib.parse

# === CONFIG ===
GNEWS_API_KEY = "5a057fbc085dd87985b068336a96375e"  # Replace with your actual key from https://gnews.io/ 
GNEWS_API_URL = "https://gnews.io/api/v4/search"

# === PAGE SETUP ===
st.set_page_config(page_title="Coalition President News Dashboard", layout="wide")
st.title("🗞️ President News Dashboard")

# === INPUT SECTION ===
st.sidebar.header("Upload President List")
uploaded_file = st.sidebar.file_uploader("Upload a CSV with Institution, Title, First, Last", type=["csv"])

# === LOAD DATA ===
if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8', errors='replace')
else:
    st.sidebar.warning("Please upload a CSV to display results.")
    st.stop()

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

# === DISPLAY RESULTS ===
for index, row in df.iterrows():
    first = row["First"]
    last = row["Last"]
    institution = row["Institution"]
    full_name = f"{first} {last}"

    articles = fetch_news(first, last, institution)

    if not articles:
        with st.expander(f"{full_name} – {institution}"):
            st.write("No recent news found.")
    else:
        st.markdown(f"## 🟢 {full_name} – {institution}")
        for article in articles:
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.markdown(f"*{article.get('publishedAt', 'No date')}* — {article.get('source', {}).get('name', 'Unknown Source')}")
            st.write(article.get("description", "No description available."))
            st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.caption("Created with ❤️ using Streamlit + GNews API")
