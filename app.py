import streamlit as st

from utils.data import load_data

st.set_page_config(
    page_title="SO Developer Survey — Interactive EDA",
    page_icon="📊",
    layout="wide",
)

df, meta = load_data()

st.title("Stack Overflow Developer Survey — Interactive EDA")
st.markdown(
    f"**Dataset:** Stack Overflow Developer Survey 2024/2025 &nbsp;·&nbsp; "
    f"**{len(df):,} respondents** &nbsp;·&nbsp; "
    f"**{len(df.columns)} columns**"
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Theme 1 — AI Adoption × Compensation")
    st.markdown(
        "Explore how AI tool usage frequency relates to developer salaries "
        "across countries and developer types.\n\n"
        "**Charts:** Violin · Bubble · Diverging Bar"
    )

with col2:
    st.subheader("Theme 2 — AI Adoption × Tech Stack")
    st.markdown(
        "Discover which language communities are most AI-forward "
        "and which AI models they prefer.\n\n"
        "**Charts:** Lollipop · Heatmap · Slope"
    )

st.divider()
st.subheader("Key Findings")
st.markdown(
    "1. **AI adoption correlates with higher compensation** — daily AI users command "
    "measurably higher salaries, with the largest premiums in senior engineering and DevOps roles.\n"
    "2. **High-income countries lead both AI adoption and pay** — a clear positive trend shows "
    "that AI tool access and economic context reinforce each other globally.\n"
    "3. **AI adoption is not uniform across tech stacks** — modern ecosystems (Rust, Kotlin, "
    "TypeScript) are more AI-forward; Python communities explore a broader model palette than "
    "any other language community."
)

st.info("Use the sidebar to navigate between pages.")
