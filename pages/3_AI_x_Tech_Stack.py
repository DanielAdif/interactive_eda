import streamlit as st

from utils.charts import chart4_lollipop_lang, chart5_heatmap_lang_model, chart6_slope_ai_momentum
from utils.data import load_data

st.set_page_config(page_title="AI × Tech Stack", page_icon="💻", layout="wide")
st.title("AI Adoption × Tech Stack")

df, meta = load_data()

# --- Sidebar (chart parameters, not row-level filters) ---
st.sidebar.header("Chart Parameters")
top_langs = st.sidebar.slider("Top N Languages (Charts 4 & 5)", 5, 20, 15)
top_models = st.sidebar.slider("Top N AI Models (Chart 5)", 3, 8, 5)
min_resp = st.sidebar.slider("Min Respondents per Language (Chart 6)", 10, 100, 20)

# --- Chart 4 ---
st.subheader("Chart 4 — AI Adoption Rate by Programming Language")
fig4 = chart4_lollipop_lang(meta["lang_have"], top_n=top_langs)
if not fig4.data:
    st.warning("No data available for the lollipop chart with the current parameters.")
else:
    st.plotly_chart(fig4, use_container_width=True)
st.markdown(
    "**Insight:** Rust, Kotlin, and TypeScript communities show the highest AI adoption rates. "
    "Legacy languages fall below the overall average, consistent with their more conservative user bases."
)

st.divider()

# --- Chart 5 ---
st.subheader("Chart 5 — AI Model Usage Across Language Communities")
fig5 = chart5_heatmap_lang_model(meta["lang_have"], top_langs=top_langs, top_models=top_models)
if not fig5.data:
    st.warning("No data available for the heatmap with the current parameters.")
else:
    st.plotly_chart(fig5, use_container_width=True)
st.markdown(
    "**Insight:** ChatGPT/GPT models dominate across every language community, but Python "
    "developers explore a broader model palette — Claude, Gemini — reflecting their AI/ML focus."
)

st.divider()

# --- Chart 6 ---
st.subheader("Chart 6 — AI Adoption Momentum: Current vs. Aspiring Users")
fig6 = chart6_slope_ai_momentum(meta["lang_have"], meta["lang_want"], min_respondents=min_resp)
if not fig6.data:
    st.warning("No data available for the slope chart. Try lowering the min respondents slider.")
else:
    st.plotly_chart(fig6, use_container_width=True)
st.markdown(
    "**Insight:** Languages with rising slopes are attracting AI-native developers into their "
    "future user cohorts, signalling which ecosystems are most AI-forward next."
)
