import pandas as pd
import numpy as np
import pytest
from utils.data import _explode_col, _prepare, shorten_ai_label


class TestExplodeCol:
    def test_splits_on_semicolon(self, sample_df):
        result = _explode_col(sample_df, "LanguageHaveWorkedWith")
        langs = result["LanguageHaveWorkedWith"].tolist()
        assert "Python" in langs
        assert "JavaScript" in langs
        assert "Java" in langs

    def test_drops_nan_rows(self, sample_df):
        result = _explode_col(sample_df, "LanguageHaveWorkedWith")
        assert result["LanguageHaveWorkedWith"].isna().sum() == 0

    def test_strips_whitespace(self, sample_df):
        df = sample_df.copy()
        df.loc[0, "LanguageHaveWorkedWith"] = " Python ; JavaScript "
        result = _explode_col(df, "LanguageHaveWorkedWith")
        assert "Python" in result["LanguageHaveWorkedWith"].values
        assert " Python " not in result["LanguageHaveWorkedWith"].values

    def test_preserves_other_columns(self, sample_df):
        result = _explode_col(sample_df, "LanguageHaveWorkedWith")
        assert "ConvertedCompYearly" in result.columns
        assert "Country" in result.columns


class TestPrepare:
    def test_adds_is_ai_user_column(self, sample_df):
        df, _ = _prepare(sample_df.copy())
        assert "is_ai_user" in df.columns

    def test_is_ai_user_true_for_yes_responses(self, sample_df):
        df, _ = _prepare(sample_df.copy())
        # "I use it frequently, almost daily" → no "yes" → False
        # "Yes, but I rarely use it" → contains "yes" → True
        assert df.loc[df["AISelect"] == "Yes, but I rarely use it (less than once a week)", "is_ai_user"].iloc[0] == True

    def test_is_ai_user_false_for_no_responses(self, sample_df):
        df, _ = _prepare(sample_df.copy())
        assert df.loc[df["AISelect"] == "No, and I don't plan to", "is_ai_user"].iloc[0] == False

    def test_coerces_yearscode_to_numeric(self, sample_df):
        df, _ = _prepare(sample_df.copy())
        assert pd.api.types.is_float_dtype(df["YearsCode"])
        assert pd.isna(df.loc[df["YearsCode"].isna(), "YearsCode"]).all()

    def test_meta_contains_expected_keys(self, sample_df):
        _, meta = _prepare(sample_df.copy())
        assert "lang_have" in meta
        assert "lang_want" in meta
        assert "ai_models" in meta
        assert "dev_types" in meta

    def test_lang_have_exploded(self, sample_df):
        _, meta = _prepare(sample_df.copy())
        assert "Python" in meta["lang_have"]["LanguageHaveWorkedWith"].values


class TestShortenAiLabel:
    def test_daily(self):
        assert shorten_ai_label("I use it frequently, almost daily") == "Daily"

    def test_weekly(self):
        assert shorten_ai_label("Yes, I use it occasionally (1-4 times per week)") == "Weekly"

    def test_monthly(self):
        assert shorten_ai_label("Yes, but I rarely use it (less than once a week)") == "Monthly"

    def test_planning(self):
        assert shorten_ai_label("No, but I plan to soon") == "Planning"

    def test_never(self):
        assert shorten_ai_label("No, and I don't plan to") == "Never"
