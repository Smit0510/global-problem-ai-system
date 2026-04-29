import os
import pandas as pd
import subprocess
import streamlit as st

@st.cache_data
def load_data():

    if not os.path.exists("data/discussions_clustered.csv"):
        st.info("Generating data with AI pipeline...")
        subprocess.run(["python", "advanced_run_pipeline.py"])

    discussions = pd.read_csv("data/discussions_clustered.csv")
    rankings = pd.read_csv("data/problem_rankings.csv")
    opportunities = pd.read_csv("data/opportunity_scores.csv")
    ideas = pd.read_csv("data/startup_ideas.csv")
    market = pd.read_csv("data/market_analysis.csv")

    return discussions, rankings, opportunities, ideas, market
