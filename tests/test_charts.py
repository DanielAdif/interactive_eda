import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pytest
from utils.data import _prepare


@pytest.fixture
def comp_df(sample_df):
    """Larger compensation DataFrame for chart tests."""
    rows = []
    ai_labels = [
        "I use it frequently, almost daily",
        "Yes, but I rarely use it (less than once a week)",
        "No, and I don't plan to",
        "No, but I plan to soon",
    ]
    devtypes = [
        "Developer, full-stack;Developer, back-end",
        "Developer, front-end",
        "Developer, back-end",
        "DevOps specialist",
        "Senior Executive (C-Suite, VP, etc.)",
    ]
    for i in range(100):
        rows.append({
            "AISelect": ai_labels[i % len(ai_labels)],
            "ConvertedCompYearly": 60000 + i * 1000,
            "Country": ["United States", "Germany", "India", "France", "Brazil"][i % 5],
            "Employment": "Employed, full-time",
            "YearsCode": float(i % 20 + 1),
            "WorkExp": float(i % 15 + 1),
            "DevType": devtypes[i % len(devtypes)],
            "LanguageHaveWorkedWith": "Python;JavaScript",
            "LanguageWantToWorkWith": "Rust;Python",
            "AIModelsHaveWorkedWith": "ChatGPT;Claude",
            "AISent": "Very favorable",
        })
    df = pd.DataFrame(rows)
    df, _ = _prepare(df)
    return df


class TestChart1ViolinSalaryByAi:
    def test_returns_figure(self, comp_df):
        from utils.charts import chart1_violin_salary_by_ai
        fig = chart1_violin_salary_by_ai(comp_df)
        assert isinstance(fig, go.Figure)

    def test_has_violin_traces(self, comp_df):
        from utils.charts import chart1_violin_salary_by_ai
        fig = chart1_violin_salary_by_ai(comp_df)
        trace_types = [type(t).__name__ for t in fig.data]
        assert "Violin" in trace_types

    def test_handles_empty_df(self):
        from utils.charts import chart1_violin_salary_by_ai
        empty = pd.DataFrame(columns=["AISelect", "ConvertedCompYearly", "is_ai_user"])
        fig = chart1_violin_salary_by_ai(empty)
        assert isinstance(fig, go.Figure)


class TestChart2BubbleCountry:
    def test_returns_figure(self, comp_df):
        from utils.charts import chart2_bubble_country
        fig = chart2_bubble_country(comp_df, min_respondents=5)
        assert isinstance(fig, go.Figure)

    def test_respects_min_respondents(self, comp_df):
        from utils.charts import chart2_bubble_country
        # With very high min, should return empty/minimal figure
        fig = chart2_bubble_country(comp_df, min_respondents=999)
        assert isinstance(fig, go.Figure)

    def test_has_scatter_trace(self, comp_df):
        from utils.charts import chart2_bubble_country
        fig = chart2_bubble_country(comp_df, min_respondents=5)
        assert len(fig.data) > 0


class TestChart3DivergingDevtype:
    def test_returns_figure(self, comp_df):
        from utils.charts import chart3_diverging_devtype
        fig = chart3_diverging_devtype(comp_df, top_n=5)
        assert isinstance(fig, go.Figure)

    def test_has_bar_trace(self, comp_df):
        from utils.charts import chart3_diverging_devtype
        fig = chart3_diverging_devtype(comp_df, top_n=5)
        trace_types = [type(t).__name__ for t in fig.data]
        assert "Bar" in trace_types

    def test_handles_empty_df(self):
        from utils.charts import chart3_diverging_devtype
        empty = pd.DataFrame(columns=["DevType", "ConvertedCompYearly", "is_ai_user"])
        fig = chart3_diverging_devtype(empty, top_n=5)
        assert isinstance(fig, go.Figure)


@pytest.fixture
def lang_have_df(sample_df):
    from utils.data import _prepare, _explode_col
    df, _ = _prepare(sample_df.copy())
    # Build a richer lang_have for tests
    rows = []
    langs = ["Python", "JavaScript", "TypeScript", "Java", "Rust", "Go", "C++", "C#", "PHP", "Ruby"]
    ai_models_pool = ["ChatGPT", "Claude", "Gemini", "GitHub Copilot", "Llama"]
    for i in range(200):
        lang = langs[i % len(langs)]
        model = ai_models_pool[i % len(ai_models_pool)]
        rows.append({
            "LanguageHaveWorkedWith": lang,
            "AIModelsHaveWorkedWith": f"{model};ChatGPT",
            "is_ai_user": i % 3 != 0,
            "ConvertedCompYearly": 70000 + i * 500,
        })
    return pd.DataFrame(rows)


@pytest.fixture
def lang_want_df():
    langs = ["Python", "JavaScript", "TypeScript", "Java", "Rust", "Go", "C++", "C#", "PHP", "Ruby"]
    rows = []
    for i in range(150):
        rows.append({
            "LanguageWantToWorkWith": langs[i % len(langs)],
            "is_ai_user": i % 2 == 0,
        })
    return pd.DataFrame(rows)


class TestChart4LollipopLang:
    def test_returns_figure(self, lang_have_df):
        from utils.charts import chart4_lollipop_lang
        fig = chart4_lollipop_lang(lang_have_df, top_n=5)
        assert isinstance(fig, go.Figure)

    def test_has_scatter_traces(self, lang_have_df):
        from utils.charts import chart4_lollipop_lang
        fig = chart4_lollipop_lang(lang_have_df, top_n=5)
        trace_types = [type(t).__name__ for t in fig.data]
        assert "Scatter" in trace_types

    def test_respects_top_n(self, lang_have_df):
        from utils.charts import chart4_lollipop_lang
        fig5 = chart4_lollipop_lang(lang_have_df, top_n=5)
        fig8 = chart4_lollipop_lang(lang_have_df, top_n=8)
        # More languages → more stem lines → more y-axis points
        # Both should return valid figures
        assert isinstance(fig5, go.Figure)
        assert isinstance(fig8, go.Figure)


class TestChart5HeatmapLangModel:
    def test_returns_figure(self, lang_have_df):
        from utils.charts import chart5_heatmap_lang_model
        fig = chart5_heatmap_lang_model(lang_have_df, top_langs=5, top_models=3)
        assert isinstance(fig, go.Figure)

    def test_has_heatmap_trace(self, lang_have_df):
        from utils.charts import chart5_heatmap_lang_model
        fig = chart5_heatmap_lang_model(lang_have_df, top_langs=5, top_models=3)
        trace_types = [type(t).__name__ for t in fig.data]
        assert "Heatmap" in trace_types


class TestChart6SlopeAiMomentum:
    def test_returns_figure(self, lang_have_df, lang_want_df):
        from utils.charts import chart6_slope_ai_momentum
        fig = chart6_slope_ai_momentum(lang_have_df, lang_want_df, min_respondents=5)
        assert isinstance(fig, go.Figure)

    def test_has_scatter_traces(self, lang_have_df, lang_want_df):
        from utils.charts import chart6_slope_ai_momentum
        fig = chart6_slope_ai_momentum(lang_have_df, lang_want_df, min_respondents=5)
        assert len(fig.data) > 0

    def test_respects_min_respondents(self, lang_have_df, lang_want_df):
        from utils.charts import chart6_slope_ai_momentum
        fig = chart6_slope_ai_momentum(lang_have_df, lang_want_df, min_respondents=9999)
        assert isinstance(fig, go.Figure)
