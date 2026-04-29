import os
import pandas as pd
import subprocess
import streamlit as st

@st.cache_data
def load_data():

    if not os.path.exists("data/discussions_clustered.csv"):
        st.write("Generating data...")
        subprocess.run(["python", "src/advanced_run_pipeline.py"])

    discussions = pd.read_csv("data/discussions_clustered.csv")
    rankings = pd.read_csv("data/problem_rankings.csv")
    opportunities = pd.read_csv("data/opportunity_scores.csv")
    ideas = pd.read_csv("data/startup_ideas.csv")
    market = pd.read_csv("data/market_analysis.csv")

    return discussions, rankings, opportunities, ideas, market

discussions, rankings, opportunities, ideas, market = load_data()

st.subheader("Top Startup Problems")
st.dataframe(rankings.head(10))

st.subheader("Startup Ideas")
st.dataframe(ideas.head(10))
