import streamlit as st
import os
import pandas as pd
import subprocess

st.title("AI Problem Discovery Dashboard")

st.write("App started successfully")

@st.cache_data
def load_data():

    st.write("Checking for data files...")

    os.makedirs("data", exist_ok=True)

    if not os.path.exists("data/discussions_clustered.csv"):
        st.write("Data not found. Running pipeline...")
        subprocess.run(["python", "advanced_run_pipeline.py"])

    if not os.path.exists("data/discussions_clustered.csv"):
        st.error("Pipeline did not generate data.")
        st.stop()

    st.write("Loading CSV files...")

    discussions = pd.read_csv("data/discussions_clustered.csv")
    rankings = pd.read_csv("data/problem_rankings.csv")
    opportunities = pd.read_csv("data/opportunity_scores.csv")
    ideas = pd.read_csv("data/startup_ideas.csv")
    market = pd.read_csv("data/market_analysis.csv")

    return discussions, rankings, opportunities, ideas, market


discussions, rankings, opportunities, ideas, market = load_data()

st.subheader("Top Problems")
st.dataframe(rankings.head())

st.subheader("Startup Ideas")
st.dataframe(ideas.head())
