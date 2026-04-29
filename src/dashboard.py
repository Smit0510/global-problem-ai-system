import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Problem Discovery AI", layout="wide")

st.title("🌍 Global Problem Discovery AI")
st.write("AI that scans global discussions and discovers startup opportunities.")

# -------------------------------
# Load Data
# -------------------------------

@st.cache_data
def load_data():
    discussions = pd.read_csv("data/discussions_clustered.csv")
    rankings = pd.read_csv("data/problem_rankings.csv")
    opportunities = pd.read_csv("data/opportunity_scores.csv")
    ideas = pd.read_csv("data/startup_ideas.csv")
    market = pd.read_csv("data/market_analysis.csv")
    return discussions, rankings, opportunities, ideas, market


discussions, rankings, opportunities, ideas, market = load_data()


# -------------------------------
# Top Global Problems
# -------------------------------

st.header("🔥 Top Global Problems")

top_clusters = rankings.sort_values(by="popularity", ascending=False).head(10)

for _, row in top_clusters.iterrows():
    st.write(f"**Cluster {row['cluster']} — {row['popularity']} discussions**")


st.divider()


# -------------------------------
# Problem Explorer
# -------------------------------

st.header("🚨 Problem Explorer")

cluster_ids = sorted(discussions["cluster"].unique())

selected_cluster = st.selectbox("Select Problem Cluster", cluster_ids)

cluster_data = discussions[discussions["cluster"] == selected_cluster]

popularity = rankings[rankings["cluster"] == selected_cluster]["popularity"].values
popularity = popularity[0] if len(popularity) > 0 else 0

opportunity = opportunities[opportunities["cluster"] == selected_cluster]["opportunity_score"].values
opportunity = opportunity[0] if len(opportunity) > 0 else 0


col1, col2 = st.columns(2)

with col1:
    st.metric("📊 Popularity Score", popularity)

with col2:
    st.metric("🚀 Opportunity Score", f"{opportunity:.2f}/100")


# -------------------------------
# Example Discussions
# -------------------------------

st.subheader("💬 Example Discussions")

sample_posts = cluster_data["text"].head(5)

for post in sample_posts:
    st.write(f"- {post}")


st.divider()


# -------------------------------
# AI Startup Idea
# -------------------------------

st.subheader("🚀 AI Startup Opportunity")

idea_row = ideas[ideas["cluster"] == selected_cluster]

if len(idea_row) > 0:
    st.write(idea_row.iloc[0]["idea"])
else:
    st.write("No startup idea generated yet.")

# -------------------------------
# AI Market Idea
# -------------------------------

st.subheader("📊 Market Analysis")

market_row = market[market["cluster"] == selected_cluster]

if not market_row.empty:
    st.write(market_row["market_analysis"].values[0])
else:
    st.write("Market analysis not available yet.")