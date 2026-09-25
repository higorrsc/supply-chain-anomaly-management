import json
import os
from typing import Any

import altair as alt
import httpx
import pandas as pd
import streamlit as st

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="Supply Chain Anomalies",
    page_icon=":material/monitoring:",
    layout="wide",
)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
ANOMALIES_ENDPOINT = f"{API_URL}/api/v1/anomalies"
ITEMS_ENDPOINT = f"{API_URL}/api/v1/items"


@st.cache_data(ttl="5m", show_spinner="Fetching anomalies...")
def fetch_anomalies(page_size: int = 100) -> list[dict[str, Any]]:
    """Fetch recent anomalies from the API."""
    try:
        response = httpx.get(
            ANOMALIES_ENDPOINT,
            params={"page": 1, "page_size": page_size},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        return list(data.get("data", []))
    except Exception as e:
        st.error(f"Failed to fetch anomalies from API: {e}")
        return []


@st.cache_data(ttl="15m", show_spinner="Fetching items mapping...")
def fetch_items_mapping() -> dict[str, str]:
    """Fetch all items and build a mapping of id -> description."""
    try:
        response = httpx.get(
            ITEMS_ENDPOINT,
            params={"page": 1, "page_size": 100},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return {item["id"]: f"{item['sku']} - {item['description']}" for item in data}
    except Exception as e:
        st.warning(f"Failed to fetch items from API: {e}")
        return {}


def render_page_header(title: str) -> None:
    """Render page header with title and reset button."""
    with st.container(horizontal=True, vertical_alignment="center"):
        st.title(title)
        st.markdown(
            "[Open FastAPI Swagger :material/open_in_new:](/docs)",
            unsafe_allow_html=False,
        )
        if st.button(":material/refresh: Refresh", type="tertiary"):
            st.cache_data.clear()
            st.rerun()


# --- Main Layout ---
render_page_header("Supply Chain Anomalies")

# Load Data
raw_anomalies = fetch_anomalies(page_size=100)
items_map = fetch_items_mapping()

if not raw_anomalies:
    st.info("No anomalies found or API is unreachable.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(raw_anomalies)

# Convert types
df["detected_at"] = pd.to_datetime(df["detected_at"])
df["score"] = pd.to_numeric(df["score"])
df["status"] = df["status"].str.upper()
df["severity"] = df["severity"].str.upper()

# Add Item Description and Raw JSON
df["item_description"] = df["item_id"].apply(lambda x: items_map.get(str(x), str(x)))
df["raw_details"] = df.apply(lambda row: json.dumps(row.to_dict(), default=str), axis=1)

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filters")

    # Date range filter
    min_date = df["detected_at"].min().date()
    max_date = df["detected_at"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Severity filter
    all_severities = df["severity"].unique().tolist()
    selected_severities = st.multiselect(
        "Severity",
        options=all_severities,
        default=all_severities,
    )

    # Status filter
    all_statuses = df["status"].unique().tolist()
    selected_statuses = st.multiselect(
        "Status",
        options=all_statuses,
        default=all_statuses,
    )

# Apply Filters
filtered_df = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["detected_at"].dt.date >= start_date)
        & (filtered_df["detected_at"].dt.date <= end_date)
    ]

if selected_severities:
    filtered_df = filtered_df[filtered_df["severity"].isin(selected_severities)]

if selected_statuses:
    filtered_df = filtered_df[filtered_df["status"].isin(selected_statuses)]

# --- KPIs ---
st.subheader("Overview")
with st.container(horizontal=True):
    total_anomalies = len(filtered_df)
    avg_score = filtered_df["score"].mean() if total_anomalies > 0 else 0
    resolved_count = len(filtered_df[filtered_df["status"] == "RESOLVED"])

    st.metric("Total Anomalies", f"{total_anomalies}", border=True)
    st.metric("Avg Score", f"{avg_score:.1f}", border=True)
    st.metric("Resolved", f"{resolved_count}", border=True)

# --- Charts ---
col1, col2 = st.columns(2)

with col1, st.container(border=True):
    st.subheader("Anomalies by Severity")
    if not filtered_df.empty:
        severity_counts = filtered_df["severity"].value_counts().reset_index()
        severity_counts.columns = ["Severity", "Count"]

        chart = (
            alt.Chart(severity_counts)
            .mark_bar()
            .encode(
                x=alt.X("Severity:N", sort="-y"),
                y=alt.Y("Count:Q"),
                color=alt.Color("Severity:N", legend=None),
                tooltip=["Severity", "Count"],
            )
        )
        st.altair_chart(chart, width="stretch")
    else:
        st.write("No data available.")

with col2, st.container(border=True):
    st.subheader("Anomalies Over Time")
    if not filtered_df.empty:
        time_df = filtered_df.copy()
        time_df["date"] = time_df["detected_at"].dt.date
        daily_counts = time_df.groupby("date").size().reset_index(name="Count")

        chart = (
            alt.Chart(daily_counts)
            .mark_line(point=True)
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("Count:Q", title="Anomalies"),
                tooltip=["date", "Count"],
            )
        )
        st.altair_chart(chart, width="stretch")
    else:
        st.write("No data available.")

# --- Data Table ---
with st.container(border=True):
    st.subheader("Anomaly Details")

    display_df = filtered_df[
        [
            "detected_at",
            "severity",
            "score",
            "status",
            "item_description",
            "raw_details",
        ]
    ].sort_values("detected_at", ascending=False)

    st.dataframe(
        display_df,
        column_config={
            "detected_at": st.column_config.DatetimeColumn(
                "Detected At", format="YYYY-MM-DD HH:mm:ss"
            ),
            "severity": "Severity",
            "score": st.column_config.NumberColumn("Score", format="%.2f"),
            "status": "Status",
            "item_description": "Item",
            "raw_details": "Raw Details (JSON)",
        },
        hide_index=True,
    )
