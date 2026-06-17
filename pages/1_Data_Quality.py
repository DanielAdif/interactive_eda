import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.data import load_data

st.set_page_config(page_title="Data Quality", page_icon="🔍", layout="wide")
st.title("Data Quality")

df, _meta = load_data()

# --- Missing values heatmap ---
st.subheader("Missing Values")
missing = df.isnull().astype(int)
fig_missing = go.Figure(go.Heatmap(
    z=missing.T.values,
    x=list(range(len(df))),
    y=missing.columns.tolist(),
    colorscale=[[0, "#f0f0f0"], [1, "#e76f51"]],
    showscale=False,
    hovertemplate="Column: %{y}<br>Row: %{x}<br>Missing: %{z}<extra></extra>",
))
fig_missing.update_layout(
    title="Missing Values Heatmap (orange = missing)",
    xaxis_title="Row index",
    yaxis_title="Column",
    height=600,
    template="plotly_white",
)
st.plotly_chart(fig_missing, use_container_width=True)

# --- Summary metrics ---
st.subheader("Column Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Total Rows", f"{len(df):,}")
m2.metric("Total Columns", len(df.columns))
m3.metric("Duplicate Rows", int(df.duplicated().sum()))

quality = (
    pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "null_count": df.isnull().sum(),
        "null_pct": (df.isnull().sum() / len(df) * 100).round(1),
    })
    .sort_values("null_pct", ascending=False)
    .reset_index()
    .rename(columns={"index": "column"})
)
st.dataframe(quality, use_container_width=True, height=400)

# --- Descriptive stats ---
st.subheader("Descriptive Statistics — Key Numeric Columns")
stats = df[["ConvertedCompYearly", "YearsCode", "WorkExp"]].describe().round(1)
st.dataframe(stats, use_container_width=True)
