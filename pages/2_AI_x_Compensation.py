import streamlit as st

from utils.charts import chart1_violin_salary_by_ai, chart2_bubble_country, chart3_diverging_devtype
from utils.data import load_data

st.set_page_config(page_title="AI × Compensation", page_icon="💰", layout="wide")
st.title("AI Adoption × Compensation")

df, _meta = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")

employment_options = sorted(df["Employment"].dropna().unique().tolist())
selected_employment = st.sidebar.multiselect(
    "Employment Type",
    options=employment_options,
    default=employment_options,
)

yr_min = int(df["YearsCode"].min(skipna=True))
yr_max = int(df["YearsCode"].max(skipna=True))
yr_range = st.sidebar.slider("Years of Experience", yr_min, yr_max, (yr_min, yr_max))

p99 = int(df["ConvertedCompYearly"].quantile(0.99))
comp_cap = st.sidebar.slider(
    "Compensation Cap (USD)", 50_000, 500_000, p99, step=10_000,
    format="$%d",
)

st.sidebar.markdown("---")
st.sidebar.subheader("Chart Options")
min_resp = st.sidebar.slider("Min Respondents per Country (Chart 2)", 5, 50, 10)
top_n_devtype = st.sidebar.slider("Top N Developer Types (Chart 3)", 5, 15, 10)

# --- Apply filters ---
filtered = df.copy()
if selected_employment:
    filtered = filtered[filtered["Employment"].isin(selected_employment)]
filtered = filtered[
    filtered["YearsCode"].isna() | filtered["YearsCode"].between(yr_range[0], yr_range[1])
]
filtered = filtered[
    filtered["ConvertedCompYearly"].isna() | (filtered["ConvertedCompYearly"] <= comp_cap)
]

if filtered.empty:
    st.warning("No data matches the current filters. Adjust the sidebar controls.")
    st.stop()

st.caption(f"**{len(filtered):,}** respondents match the current filters.")

# --- Chart 1 ---
st.subheader("Chart 1 — Salary Distribution by AI Usage Frequency")
st.plotly_chart(chart1_violin_salary_by_ai(filtered), use_container_width=True)
st.markdown(
    "**Insight:** Daily AI users show a notably higher and tighter salary distribution "
    "than non-users, suggesting AI tool proficiency correlates with seniority and compensation."
)

st.divider()

# --- Chart 2 ---
st.subheader("Chart 2 — Country AI Adoption Rate vs. Median Salary")
st.plotly_chart(chart2_bubble_country(filtered, min_respondents=min_resp), use_container_width=True)
st.markdown(
    "**Insight:** High-income countries cluster in the top-right quadrant — high AI adoption "
    "and high pay — suggesting AI access and economic context reinforce each other."
)

st.divider()

# --- Chart 3 ---
st.subheader("Chart 3 — AI Salary Premium by Developer Type")
st.plotly_chart(chart3_diverging_devtype(filtered, top_n=top_n_devtype), use_container_width=True)
st.markdown(
    "**Insight:** Senior engineers and DevOps specialists who adopt AI tools show the "
    "largest salary premium over their non-adopting peers."
)
