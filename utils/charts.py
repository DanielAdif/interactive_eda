from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data import shorten_ai_label

TEAL = "#2a9d8f"
CORAL = "#e76f51"
TEMPLATE = "plotly_white"


def chart1_violin_salary_by_ai(df: pd.DataFrame) -> go.Figure:
    comp = df[["AISelect", "ConvertedCompYearly"]].dropna().copy()
    if comp.empty:
        return go.Figure()
    p99 = comp["ConvertedCompYearly"].quantile(0.99)
    comp = comp[comp["ConvertedCompYearly"] <= p99].copy()
    comp["AI_Usage"] = comp["AISelect"].map(shorten_ai_label)
    order = [o for o in ["Never", "Planning", "Monthly", "Weekly", "Daily"]
             if o in comp["AI_Usage"].unique()]
    if not order:
        return go.Figure()

    palette = px.colors.qualitative.Set2
    fig = go.Figure()
    for i, cat in enumerate(order):
        subset = comp[comp["AI_Usage"] == cat]["ConvertedCompYearly"]
        fig.add_trace(go.Violin(
            y=subset,
            name=cat,
            points="all",
            pointpos=0,
            jitter=0.3,
            marker=dict(opacity=0.25, size=3),
            line_color=palette[i % len(palette)],
            fillcolor=palette[i % len(palette)],
            box_visible=True,
            meanline_visible=True,
            hovertemplate=f"<b>{cat}</b><br>Salary: $%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_yaxes(type="log", tickprefix="$", tickformat=",.0f")
    fig.update_layout(
        title="Salary Distribution by AI Usage Frequency",
        yaxis_title="Annual Compensation (USD, log scale)",
        xaxis_title="AI Usage Frequency",
        template=TEMPLATE,
        showlegend=False,
    )
    return fig


def chart2_bubble_country(df: pd.DataFrame, min_respondents: int = 10) -> go.Figure:
    country = (
        df.groupby("Country")
        .agg(
            ai_rate=("is_ai_user", "mean"),
            median_comp=("ConvertedCompYearly", "median"),
            n=("Country", "count"),
        )
        .reset_index()
    )
    country = country[
        (country["n"] >= min_respondents) & country["median_comp"].notna()
    ].copy()
    if country.empty:
        return go.Figure()

    fig = px.scatter(
        country,
        x="ai_rate",
        y="median_comp",
        size="n",
        color="median_comp",
        color_continuous_scale="Viridis",
        hover_name="Country",
        hover_data={"ai_rate": ":.1%", "median_comp": ":$,.0f", "n": True},
        labels={
            "ai_rate": "AI Adoption Rate",
            "median_comp": "Median Annual Comp (USD)",
            "n": "Respondents",
        },
        title="Country-Level AI Adoption Rate vs. Median Salary"
              "<br><sup>Bubble size = respondent count</sup>",
        template=TEMPLATE,
    )
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


def chart3_diverging_devtype(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    devtype = (
        df[["DevType", "ConvertedCompYearly", "is_ai_user"]]
        .dropna(subset=["ConvertedCompYearly", "DevType"])
        .copy()
    )
    devtype["DevType"] = devtype["DevType"].str.split(";")
    devtype = devtype.explode("DevType")
    devtype["DevType"] = devtype["DevType"].str.strip()

    top = devtype["DevType"].value_counts().head(top_n).index.tolist()
    devtype = devtype[devtype["DevType"].isin(top)]

    pivot = (
        devtype.groupby(["DevType", "is_ai_user"])["ConvertedCompYearly"]
        .median()
        .unstack("is_ai_user")
    )
    if True not in pivot.columns or False not in pivot.columns:
        return go.Figure()
    pivot.columns = ["no_ai", "ai_user"]
    pivot = pivot.dropna()
    pivot["premium"] = pivot["ai_user"] - pivot["no_ai"]
    pivot = pivot.sort_values("premium").reset_index()
    if pivot.empty:
        return go.Figure()

    colors = [TEAL if v >= 0 else CORAL for v in pivot["premium"]]
    fig = go.Figure(go.Bar(
        x=pivot["premium"],
        y=pivot["DevType"],
        orientation="h",
        marker_color=colors,
        hovertemplate="<b>%{y}</b><br>Premium: $%{x:,.0f}<extra></extra>",
    ))
    fig.add_vline(x=0, line_color="black", line_width=1)
    fig.update_layout(
        title="AI Adoption Salary Premium by Developer Type",
        xaxis_title="Salary Premium of AI Users vs. Non-Users (USD)",
        yaxis_title="Developer Type",
        template=TEMPLATE,
    )
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    return fig
