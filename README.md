# Stack Overflow Developer Survey — Interactive EDA Dashboard

> An interactive multi-page Streamlit dashboard exploring AI adoption vs. compensation and AI adoption vs. tech stack trends from the Stack Overflow Developer Survey.

## Live Demo

<!-- Replace with your Streamlit Cloud URL after deploying -->
*Deploy to Streamlit Community Cloud and paste the URL here.*

## Project Structure

```
interactive_eda/
├── app.py                     # Landing page
├── pages/
│   ├── 1_Data_Quality.py      # Missing values, column stats
│   ├── 2_AI_x_Compensation.py # Charts 1–3 with sidebar filters
│   └── 3_AI_x_Tech_Stack.py   # Charts 4–6 with parameter sliders
├── utils/
│   ├── data.py                # load_data() + shared transforms
│   └── charts.py              # 6 pure Plotly chart functions
├── dataset/
│   └── so_dev_survey.csv
├── requirements.txt
└── README.md
```

## Pages

| Page | Charts | Filters |
|------|--------|---------|
| Landing | — | — |
| Data Quality | Missing values heatmap, column table, descriptive stats | None |
| AI × Compensation | Violin, Bubble, Diverging Bar | Employment, years of experience, comp cap |
| AI × Tech Stack | Lollipop, Heatmap, Slope | Top N languages, top N models, min respondents |

## Key Findings

1. **AI adoption correlates with higher compensation** — daily AI users command measurably higher salaries, with the largest premiums in senior engineering and DevOps roles.
2. **High-income countries lead both AI adoption and pay** — a clear positive trend shows that AI tool access and economic context reinforce each other globally.
3. **AI adoption is not uniform across tech stacks** — modern ecosystems (Rust, Kotlin, TypeScript) are more AI-forward; Python communities explore a broader model palette than any other language community.

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

The browser opens automatically at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Push this repository to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select your repo, branch (`main`), and set the entry point to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically.
5. Once deployed, paste the URL into the **Live Demo** section above.

## Dataset

**Stack Overflow Developer Survey 2024/2025**
- ~2,037 respondents · ~174 columns
- Key columns: `AISelect`, `ConvertedCompYearly`, `Country`, `DevType`, `LanguageHaveWorkedWith`, `LanguageWantToWorkWith`, `AIModelsHaveWorkedWith`
- Multi-value columns are semicolon-separated and exploded at load time
