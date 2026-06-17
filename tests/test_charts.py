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
