import os
import pandas as pd
import subprocess
import streamlit as st

@st.cache_data
def load_data():

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # If data not generated, run pipeline
    if not os.path.exists("data/discussions_clustered.csv"):
        st.write("Generating data with pipeline...")
        subprocess.run(
            ["python", "advanced_run_pipeline.py"],
            cwd=".",  # run from project root
        )

    # If still missing, show error and stop
    if not os.path.exists("data/discussions_clustered.csv"):
        st.error("Data generation failed. Pipeline did not create CSV files.")
        st.stop()

    discussions = pd.read_csv("data/discussions_clustered.csv")
    rankings = pd.read_csv("data/problem_rankings.csv")
    opportunities = pd.read_csv("data/opportunity_scores.csv")
    ideas = pd.read_csv("data/startup_ideas.csv")
    market = pd.read_csv("data/market_analysis.csv")

    return discussions, rankings, opportunities, ideas, market
