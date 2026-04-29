import streamlit as st
import os
import pandas as pd
import subprocess

st.title("AI Problem Discovery Dashboard")

st.write("App started successfully")

@st.cache_data
def load_data():

    discussions = pd.read_csv("data/discussions_clustered.csv")
    rankings = pd.read_csv("data/problem_rankings.csv")
    opportunities = pd.read_csv("data/opportunity_scores.csv")
    ideas = pd.read_csv("data/startup_ideas.csv")
    market = pd.read_csv("data/market_analysis.csv")

    return discussions, rankings, opportunities, ideas, market
