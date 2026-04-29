import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AI Problem Discovery Dashboard", layout="wide")

st.title("AI Problem Discovery Dashboard")

st.write("Discover trending problems and startup opportunities using AI.")

DATA_PATH = "data"

def load_csv(file):
    path = os.path.join(DATA_PATH, file)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


# Load datasets
discussions = load_csv("discussions_clustered.csv")
rankings = load_csv("problem_rankings.csv")
opportunities = load_csv("opportunity_scores.csv")
ideas = load_csv("startup_ideas.csv")
market = load_csv("market_analysis.csv")


# Show message if no data
if discussions is None:
    st.warning("⚠️ No data found. Please upload CSV files to the data folder.")
    st.stop()


# Layout
tab1, tab2, tab3, tab4 = st.tabs(
    ["Problems", "Startup Ideas", "Opportunities", "Market Analysis"]
)


with tab1:
    st.subheader("Top Problems")
    if rankings is not None:
        st.dataframe(rankings)
    else:
        st.info("Problem rankings data not available.")


with tab2:
    st.subheader("Generated Startup Ideas")
    if ideas is not None:
        st.dataframe(ideas)
    else:
        st.info("Startup ideas data not available.")


with tab3:
    st.subheader("Opportunity Scores")
    if opportunities is not None:
        st.dataframe(opportunities)
    else:
        st.info("Opportunity scores data not available.")


with tab4:
    st.subheader("Market Analysis")
    if market is not None:
        st.dataframe(market)
    else:
        st.info("Market analysis data not available.")
