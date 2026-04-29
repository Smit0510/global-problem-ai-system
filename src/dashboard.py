import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="AI Problem Discovery Dashboard", layout="wide")

st.title("🚀 AI Problem Discovery Dashboard")
st.write("Discover trending problems and startup opportunities using AI.")

DATA_PATH = "data"


def load_csv(file):
    path = os.path.join(DATA_PATH, file)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


# Load data
discussions = load_csv("discussions_clustered.csv")
rankings = load_csv("problem_rankings.csv")
opportunities = load_csv("opportunity_scores.csv")
ideas = load_csv("startup_ideas.csv")
market = load_csv("market_analysis.csv")


if discussions is None:
    st.warning("⚠️ No data found. Upload CSV files to the data folder.")
    st.stop()


# Sidebar filters
st.sidebar.header("Filters")

if "cluster" in discussions.columns:
    cluster_filter = st.sidebar.selectbox(
        "Select Problem Cluster",
        ["All"] + sorted(discussions["cluster"].astype(str).unique().tolist())
    )
else:
    cluster_filter = "All"


filtered_discussions = discussions.copy()

if cluster_filter != "All":
    filtered_discussions = filtered_discussions[
        filtered_discussions["cluster"].astype(str) == cluster_filter
    ]


# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Problems", "💡 Startup Ideas", "📈 Opportunities", "📉 Market Analysis"]
)


# -------------------
# Problems Tab
# -------------------

with tab1:

    st.subheader("Trending Problems")

    if rankings is not None:
        st.dataframe(rankings)

        if "score" in rankings.columns:
            fig = px.bar(
                rankings.head(10),
                x=rankings.columns[0],
                y="score",
                title="Top Problem Scores"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Discussion Data")
    st.dataframe(filtered_discussions)


# -------------------
# Startup Ideas Tab
# -------------------

with tab2:

    st.subheader("Generated Startup Ideas")

    if ideas is not None:
        st.dataframe(ideas)

        if "idea" in ideas.columns:
            idea_select = st.selectbox("Explore Idea", ideas["idea"])

            idea_row = ideas[ideas["idea"] == idea_select]

            st.write("### Idea Details")
            st.write(idea_row)


# -------------------
# Opportunities Tab
# -------------------

with tab3:

    st.subheader("Opportunity Scores")

    if opportunities is not None:
        st.dataframe(opportunities)

        if "score" in opportunities.columns:
            fig = px.bar(
                opportunities.head(10),
                x=opportunities.columns[0],
                y="score",
                title="Top Opportunities"
            )

            st.plotly_chart(fig, use_container_width=True)


# -------------------
# Market Analysis Tab
# -------------------

with tab4:

    st.subheader("Market Analysis")

    if market is not None:
        st.dataframe(market)

        if "market_size" in market.columns:

            fig = px.scatter(
                market,
                x="market_size",
                y="competition",
                size="market_size",
                title="Market Opportunity Map"
            )

            st.plotly_chart(fig, use_container_width=True)
