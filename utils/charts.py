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


def chart4_lollipop_lang(lang_have: pd.DataFrame, top_n: int = 15) -> go.Figure:
    top_langs = (
        lang_have["LanguageHaveWorkedWith"].value_counts().head(top_n).index.tolist()
    )
    lang_stats = (
        lang_have[lang_have["LanguageHaveWorkedWith"].isin(top_langs)]
        .groupby("LanguageHaveWorkedWith")
        .agg(ai_rate=("is_ai_user", "mean"), count=("is_ai_user", "count"))
        .reset_index()
        .sort_values("ai_rate", ascending=True)
    )
    if lang_stats.empty:
        return go.Figure()

    overall = lang_have["is_ai_user"].mean()
    colors = [TEAL if r >= overall else CORAL for r in lang_stats["ai_rate"]]

    x_stems, y_stems = [], []
    for _, row in lang_stats.iterrows():
        x_stems += [0, row["ai_rate"] * 100, None]
        y_stems += [row["LanguageHaveWorkedWith"], row["LanguageHaveWorkedWith"], None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_stems, y=y_stems,
        mode="lines",
        line=dict(color="lightgray", width=2),
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=lang_stats["ai_rate"] * 100,
        y=lang_stats["LanguageHaveWorkedWith"],
        mode="markers",
        marker=dict(color=colors, size=12, line=dict(color="white", width=1.5)),
        hovertemplate=(
            "<b>%{y}</b><br>AI Adoption: %{x:.1f}%<br>"
            f"vs avg {overall * 100:.1f}%<extra></extra>"
        ),
        showlegend=False,
    ))
    fig.add_vline(x=overall * 100, line_dash="dash", line_color="black", line_width=1)
    fig.update_layout(
        title=f"AI Tool Adoption Rate by Programming Language (Top {top_n})",
        xaxis_title="AI Tool Adoption Rate (%)",
        yaxis_title="Programming Language",
        template=TEMPLATE,
        xaxis=dict(range=[0, 105]),
    )
    return fig


def chart5_heatmap_lang_model(
    lang_have: pd.DataFrame,
    top_langs: int = 10,
    top_models: int = 5,
) -> go.Figure:
    top_lang_list = (
        lang_have["LanguageHaveWorkedWith"].value_counts().head(top_langs).index.tolist()
    )
    sub = lang_have[lang_have["LanguageHaveWorkedWith"].isin(top_lang_list)].dropna(
        subset=["AIModelsHaveWorkedWith"]
    )
    if sub.empty:
        return go.Figure()

    ai_exp = sub.assign(ai_list=sub["AIModelsHaveWorkedWith"].str.split(";")).explode("ai_list")
    ai_exp["ai_list"] = ai_exp["ai_list"].str.strip()
    top_model_list = ai_exp["ai_list"].value_counts().head(top_models).index.tolist()

    records = []
    for lang in top_lang_list:
        lang_sub = lang_have[lang_have["LanguageHaveWorkedWith"] == lang].dropna(
            subset=["AIModelsHaveWorkedWith"]
        )
        n_lang = len(lang_sub)
        if n_lang == 0:
            continue
        ai_rows = lang_sub.assign(
            ai_list=lang_sub["AIModelsHaveWorkedWith"].str.split(";")
        ).explode("ai_list")
        ai_rows["ai_list"] = ai_rows["ai_list"].str.strip()
        for model in top_model_list:
            cnt = (ai_rows["ai_list"] == model).sum()
            records.append({
                "language": lang,
                "model": model,
                "pct": round(cnt / n_lang * 100, 1),
            })

    if not records:
        return go.Figure()

    heat_df = pd.DataFrame(records)
    pivot = (
        heat_df.pivot(index="language", columns="model", values="pct")
        .fillna(0)
        .reindex(index=top_lang_list, columns=top_model_list)
    )

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="YlOrRd",
        text=pivot.values.round(1),
        texttemplate="%{text:.1f}%",
        hovertemplate=(
            "<b>%{y}</b> × <b>%{x}</b><br>%{z:.1f}% of language users<extra></extra>"
        ),
        colorbar=dict(title="% of users"),
    ))
    fig.update_layout(
        title="AI Model Usage by Programming Language Community",
        xaxis_title="AI Model",
        yaxis_title="Programming Language",
        template=TEMPLATE,
        height=500,
    )
    return fig


def chart6_slope_ai_momentum(
    lang_have: pd.DataFrame,
    lang_want: pd.DataFrame,
    min_respondents: int = 20,
) -> go.Figure:
    have_rate = (
        lang_have.groupby("LanguageHaveWorkedWith")
        .agg(current_ai_rate=("is_ai_user", "mean"), current_count=("is_ai_user", "count"))
        .reset_index()
        .rename(columns={"LanguageHaveWorkedWith": "lang"})
    )
    want_rate = (
        lang_want.groupby("LanguageWantToWorkWith")
        .agg(aspiring_ai_rate=("is_ai_user", "mean"), aspiring_count=("is_ai_user", "count"))
        .reset_index()
        .rename(columns={"LanguageWantToWorkWith": "lang"})
    )

    slope_df = have_rate.merge(want_rate, on="lang")
    slope_df = slope_df[slope_df["current_count"] >= min_respondents]
    slope_df = slope_df.nlargest(10, "current_count").copy()
    slope_df["gap"] = slope_df["aspiring_ai_rate"] - slope_df["current_ai_rate"]

    if slope_df.empty:
        return go.Figure()

    gap_min = slope_df["gap"].min()
    gap_max = slope_df["gap"].max()
    gap_range = gap_max - gap_min + 1e-9

    fig = go.Figure()
    for _, row in slope_df.iterrows():
        norm = (row["gap"] - gap_min) / gap_range
        r = int(220 * (1 - norm))
        g = int(180 * norm + 40)
        color = f"rgb({r},{g},80)"
        fig.add_trace(go.Scatter(
            x=["Current Users", "Aspiring Users"],
            y=[row["current_ai_rate"] * 100, row["aspiring_ai_rate"] * 100],
            mode="lines+markers+text",
            name=row["lang"],
            line=dict(color=color, width=2.5),
            marker=dict(color=color, size=9),
            text=[row["lang"], f"{row['lang']} ({row['gap'] * 100:+.1f}pp)"],
            textposition=["middle left", "middle right"],
            hovertemplate=(
                f"<b>{row['lang']}</b><br>"
                f"Current: {row['current_ai_rate'] * 100:.1f}%<br>"
                f"Aspiring: {row['aspiring_ai_rate'] * 100:.1f}%<br>"
                f"Gap: {row['gap'] * 100:+.1f}pp<extra></extra>"
            ),
        ))

    fig.update_layout(
        title=(
            "AI Adoption Momentum: Current vs. Aspiring Users"
            "<br><sup>Green = future adopters more AI-forward, Red = less</sup>"
        ),
        yaxis_title="AI Tool Adoption Rate (%)",
        template=TEMPLATE,
        showlegend=False,
        yaxis=dict(ticksuffix="%"),
        xaxis=dict(range=[-0.35, 1.35]),
        height=550,
    )
    return fig
