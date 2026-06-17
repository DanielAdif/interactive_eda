from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATASET_PATH = Path(__file__).parent.parent / "dataset" / "so_dev_survey.csv"


def shorten_ai_label(val: str) -> str:
    v = str(val).lower()
    if "daily" in v or "almost daily" in v:
        return "Daily"
    if "month" in v or "infrequent" in v or "rarely" in v:
        return "Monthly"
    if "week" in v:
        return "Weekly"
    if "plan" in v and "don't plan" not in v:
        return "Planning"
    return "Never"


def _explode_col(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = df.dropna(subset=[col]).copy()
    out[col] = out[col].str.split(";")
    out = out.explode(col)
    out[col] = out[col].str.strip()
    return out


def _prepare(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    for col in ("YearsCode", "WorkExp"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["is_ai_user"] = df["AISelect"].str.lower().str.contains("yes", na=False)
    meta: dict[str, pd.DataFrame] = {
        "lang_have": _explode_col(df, "LanguageHaveWorkedWith"),
        "lang_want": _explode_col(df, "LanguageWantToWorkWith"),
        "ai_models": _explode_col(df, "AIModelsHaveWorkedWith"),
        "dev_types": _explode_col(df, "DevType"),
    }
    return df, meta


@st.cache_data
def load_data() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    if not DATASET_PATH.exists():
        st.error(
            f"Dataset not found at `{DATASET_PATH}`. "
            "Ensure `dataset/so_dev_survey.csv` exists in the project root."
        )
        st.stop()
    df = pd.read_csv(DATASET_PATH)
    return _prepare(df)
