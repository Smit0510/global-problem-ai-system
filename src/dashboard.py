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


# Load datasets
discussions = load_csv("discussions_clustered.csv")
rankings = load_csv("problem_rankings.csv")
opportunities = load_csv("opportunity_scores.csv")
ideas = load_csv("startup_ideas.csv")
market = load_csv("market_analysis.csv")


# Stop if no data
if discussions is None:
    st.warning("⚠️ Data not found. Please upload CSV files into the data folder.")
    st.stop()


# ----------------------
# Sidebar Filters
# ----------------------

st.sidebar.header("Filters")

cluster_filter = "All"

if "cluster" in discussions.columns:

    cluster_options = ["All"] + sorted(
        discussions["cluster"].astype(str).unique().tolist()
    )

    cluster_filter = st.sidebar.selectbox(
        "Select Problem Cluster",
        cluster_options
    )


filtered_discussions = discussions.copy()

if cluster_filter != "All":
    filtered_discussions = filtered_discussions[
        filtered_discussions["cluster"].astype(str) == cluster_filter
    ]


# ----------------------
# Tabs
# ----------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Problems", "💡 Startup Ideas", "📈 Opportunities", "📉 Market Analysis"]
)


# ----------------------
# Problems
# ----------------------

with tab1:

    st.subheader("Trending Problems")

    if rankings is not None:

        st.dataframe(rankings)

        numeric_cols = rankings.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            fig = px.bar(
                rankings.head(10),
                y=numeric_cols[0],
                title="Top Problem Scores"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Discussion Data")

    st.dataframe(filtered_discussions)


# ----------------------
# Startup Ideas
# ----------------------

with tab2:

    st.subheader("Generated Startup Ideas")

    if ideas is not None:

        st.dataframe(ideas)

        if len(ideas.columns) > 0:

            idea_select = st.selectbox(
                "Explore Idea",
                ideas.iloc[:, 0]
            )

            idea_row = ideas[ideas.iloc[:, 0] == idea_select]

            st.write("### Idea Details")

            st.dataframe(idea_row)


# ----------------------
# Opportunities
# ----------------------

with tab3:

    st.subheader("Opportunity Scores")

    if opportunities is not None:

        st.dataframe(opportunities)

        numeric_cols = opportunities.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            fig = px.bar(
                opportunities.head(10),
                y=numeric_cols[0],
                title="Top Opportunities"
            )

            st.plotly_chart(fig, use_container_width=True)


# ----------------------
# Market Analysis
# ----------------------

with tab4:

    st.subheader("Market Analysis")

    if market is not None:

        st.dataframe(market)

        numeric_cols = market.select_dtypes(include="number").columns

        if len(numeric_cols) >= 2:

            fig = px.scatter(
                market,
                x=numeric_cols[0],
                y=numeric_cols[1],
                size=numeric_cols[0],
                title="Market Opportunity Map"
            )

            st.plotly_chart(fig, use_container_width=True)
