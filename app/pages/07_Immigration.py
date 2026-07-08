import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Immigration — ESS Ireland", page_icon="\U0001F30D", layout="wide")

page_header(
    "Immigration",
    "Perceived impact of immigration on Ireland's economy, culture and quality of life.",
)

trend = load("immigration", "trend")
fig = trend_line(trend, title="Perceived impact of immigration, 2002–2023 (0–10 scale)")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig, width='stretch')

insight(
    "Attitudes toward immigration's impact on the economy, culture and quality of life were least "
    "positive in 2010, in the aftermath of the 2008 financial crisis — the economic-impact score fell to "
    "4.5, well below the more stable culture and quality-of-life scores. All three then improved steadily, "
    "reaching a high around 2021/22 (economy 6.6, culture 6.7, place to live 6.9). 2023 shows a modest "
    "decline across all three, most notably in whether immigration makes Ireland a better place to live "
    "(down to 6.3) — a possible early sign of a shift toward more restrictive attitudes, though the overall "
    "long-run trend remains positive."
)

st.subheader("Positive views of immigration, by education (2023)")
edu = load("immigration", "breakdown_education")
edu_order = ["<Lower Secondary", "Lower Secondary", "Upper Secondary", "Advanced Vocational", "Tertiary"]
fig2 = grouped_bar(
    edu,
    x="group_value",
    color="category",
    title="Share viewing immigration's impact positively (score of 6+), by education",
    order=edu_order,
)
st.plotly_chart(fig2, width='stretch')

insight(
    "Nearly 80% of respondents with tertiary education see immigration as having a positive impact on the "
    "economy, culture and quality of life, compared with only around 41% of those with the lowest level of "
    "education — a gap most pronounced (43 percentage points) in views of whether immigration makes "
    "Ireland a better place to live (80% tertiary vs. 37% lowest education)."
)

st.subheader("Positive views of immigration, by employment status (2023)")
emp = load("immigration", "breakdown_employment")
fig3 = grouped_bar(
    emp,
    x="group_value",
    color="category",
    title="Share viewing immigration's impact positively (score of 6+), by employment status",
)
st.plotly_chart(fig3, width='stretch')

insight(
    "Views vary only modestly between those in employment and those unemployed and seeking work, but "
    "across all three measures the unemployed report less favourable attitudes — a gap of 10 points on "
    "culture, 14 on the economy, and 15 on Ireland as a place to live."
)
