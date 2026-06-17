import pytest
import pandas as pd


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "AISelect": [
            "I use it frequently, almost daily",
            "No, and I don't plan to",
            "Yes, but I rarely use it (less than once a week)",
            None,
        ],
        "ConvertedCompYearly": [120000.0, 80000.0, 95000.0, None],
        "Country": ["United States", "Germany", "France", "India"],
        "Employment": [
            "Employed, full-time",
            "Self-employed",
            "Employed, full-time",
            "Employed, part-time",
        ],
        "YearsCode": ["5", "10", "More than 50 years", None],
        "WorkExp": ["3", "8", None, "1"],
        "LanguageHaveWorkedWith": ["Python;JavaScript", "Java;Python", None, "Go"],
        "LanguageWantToWorkWith": ["Rust;Python", "TypeScript", "Go", None],
        "AIModelsHaveWorkedWith": ["ChatGPT;Claude", "ChatGPT", None, "Gemini"],
        "DevType": [
            "Developer, full-stack;Developer, back-end",
            "Developer, front-end",
            None,
            "Developer, back-end",
        ],
        "AISent": ["Very favorable", "Unfavorable", None, "Favorable"],
    })
