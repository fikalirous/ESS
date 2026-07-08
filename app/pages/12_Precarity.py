import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import data_insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Precarity — ESS Ireland", page_icon="\U0001F4BC", layout="wide")

page_header(
    "Precarity",
    "Job security: 'My job is/would be secure' (2004, 2010, 2018 — this question was not asked in every "
    "round). This topic is not covered in the published report — the charts below are a direct read of the data.",
)

trend = load("precarity", "trend_job_security_percent")
band_order = [
    "Not at all true", "A little true", "Quite true", "Very true",
    "Insecure (combined: not at all/a little true)", "Secure (combined: quite/very true)",
]
combined = trend[trend["series"].isin(["Insecure (combined: not at all/a little true)", "Secure (combined: quite/very true)"])]
fig = trend_line(combined, title="Perceived job security, 2004–2018")
fig.update_yaxes(range=[0, 100], ticksuffix="%")
st.plotly_chart(fig, width='stretch')

data_insight(
    "Perceived job security collapsed during the 2010 recession: the secure share (those saying their job "
    "is 'quite' or 'very' true to be secure) fell from 77% in 2004 to 53% in 2010, before recovering to "
    "76% by 2018 — closely tracking the same economic cycle seen in trust and economic satisfaction "
    "elsewhere in this dashboard."
)

st.subheader("Job security by income quintile (2018)")
quint = load("precarity", "breakdown_income_quintile_r9_2018")
quint_combined = quint[quint["category"].isin(["Insecure (combined: not at all/a little true)", "Secure (combined: quite/very true)"])]
quint_order = ["Bottom 20%", "2nd quintile", "3rd quintile", "4th quintile", "Top 20%"]
fig2 = grouped_bar(
    quint_combined,
    x="group_value",
    color="category",
    title="Share reporting secure vs. insecure employment, by income quintile",
    barmode="stack",
    order=quint_order,
)
st.plotly_chart(fig2, width='stretch')

data_insight(
    "Job security rises steadily with income: only 66% of the bottom income quintile report secure "
    "employment, compared with 82% of the top quintile — a 16-point gap between the lowest- and "
    "highest-earning respondents."
)
