import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Life Satisfaction & Happiness — ESS Ireland", page_icon="\U0001F60A", layout="wide")

page_header(
    "Life Satisfaction and Happiness",
    "How satisfied are you with your life as a whole nowadays? Taking all things together, how happy are you?",
)

trend = load("life_satisfaction_happiness", "trend")
fig = trend_line(trend, title="Life satisfaction and happiness, 2002–2023 (0–10 scale)")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig, width='stretch')

insight(
    "Life satisfaction has stayed high across the whole period, averaging 7.4 in 2023 — unchanged from "
    "2021/22. It dipped to its lowest point, 6.6, in 2010, coinciding with the Great Recession. Happiness "
    "follows a similar pattern and, at 7.7 in 2023, is back to its pre-pandemic (2018) level — COVID-19 "
    "appears to have had surprisingly little lasting impact on reported happiness."
)

st.subheader("Life satisfaction by employment status (2023)")
emp = load("life_satisfaction_happiness", "breakdown_employment")
emp_order = ["In paid work", "Unemployed, looking for job", "Inactive (not looking for a job)", "Refusal/Don't know", "Total Population"]
fig2 = grouped_bar(
    emp,
    x="group_value",
    color="category",
    title="Share satisfied vs. dissatisfied with life, by employment status",
    barmode="stack",
    order=emp_order,
)
st.plotly_chart(fig2, width='stretch')
st.caption(
    "The 'Refusal/Don't know' group is a small residual category (respondents who didn't answer the "
    "employment question) — its low satisfaction share should be read with caution given its likely small sample size."
)

insight(
    "A greater share of those in paid work report being satisfied with life (86%) compared with the total "
    "population (85%). Those who are inactive and not looking for work report almost equally high "
    "satisfaction (85%), while those unemployed and looking for a job are markedly more dissatisfied — "
    "only 71% report being satisfied, the lowest of any group."
)
