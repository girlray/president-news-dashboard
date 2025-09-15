import streamlit as st
import pandas as pd
import requests

# === CONFIG ===
GNEWS_API_KEY = "
5a057fbc085dd87985b068336a96375e"  # Replace with your actual key from https://gnews.io/
GNEWS_API_URL = "https://gnews.io/api/v4/search"

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

# === DISPL
                st.write(article.get("description", "No description available."))
                st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.caption("Created with ❤️ using Streamlit + NewsData.io")
