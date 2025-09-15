import streamlit as st
import pandas as pd
import requests
import urllib.parse

# === CONFIG ===
NEWS_API_KEY = "pub_662681d987f848a68a7b199b5f9609b3"  # Sign up at https://newsdata.io/
NEWS_API_URL = "https://newsdata.io/api/1/news"

# === PAGE SETUP ===
st.set_page_config(page_title="President News Dashboard", layout="wide")
st.title("📰 Coalition President News Dashboard")

# === INPUT SECTION ===
st.sidebar.header("Upload President List")
uploaded_file = st.sidebar.file_uploader("Upload a CSV with Institution, Title, First, Last", type=["csv"])

# Sample fallback data
sample_data = pd.DataFrame({
    "Institution": ["American University", "Amherst College", "Augsburg University"],
    "Title": ["President", "President", "President"],
    "First": ["Jon", "Michael", "Paul"],
    "Last": ["Alger", "Elliott", "Pribbenow"]
})

# Load the data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("Using sample data — upload a CSV to replace it.")
    df = sample_data

# === SEARCH FUNCTION ===
def fetch_news(first, last, institution):
    query = f'"{first} {last}" "{institution}"'
    params = {
        "apikey": NEWS_API_KEY,
        "q": query,
        "language": "en",
        "country": "us",
        "category": "education",
        "page": 1
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        return []

# === DISPLAY RESULTS ===
for index, row in df.iterrows():
    first = row["First"]
    last = row["Last"]
    institution = row["Institution"]
    full_name = f"{first} {last}"

    with st.expander(f"🔎 {full_name} – {institution}"):
        articles = fetch_news(first, last, institution)

        if not articles:
            st.write("No recent news found.")
        else:
            for article in articles:
                st.markdown(f"### [{article['title']}]({article['link']})")
                st.markdown(f"*{article.get('pubDate', 'No date')} — {article.get('source_id', 'Unknown Source')}*")
                st.write(article.get("description", "No description available."))
                st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.caption("Created with ❤️ using Streamlit + NewsData.io")
