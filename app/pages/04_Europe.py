import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Europe — ESS Ireland", page_icon="\U0001F1EA\U0001F1FA", layout="wide")

page_header(
    "European Unification and Attachment to Europe",
    "Trust in the EU Parliament, attitudes to EU unification, and emotional attachment to Europe.",
)

trend = load("eu_attachment", "trend")
fig = trend_line(trend, title="Attitudes to Europe, 2002–2023 (0–10 scale)")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig, width='stretch')

insight(
    "Perceptions of Europe declined during the 2008–2012 economic crisis, reaching a low point around "
    "2010 — the year Ireland entered the EU-ECB-IMF Economic Adjustment Programme. Trust in the EU "
    "Parliament recovered in the years that followed."
)

st.subheader("Euroscepticism by education (2023)")
edu = load("eu_attachment", "breakdown_education")
edu_order = ["<Lower Secondary", "Lower Secondary", "Upper Secondary", "Advanced Vocational", "Tertiary"]
cat_order = ["Low trust in EU Parliament", "Unification has gone far enough", "Low attachment to Europe"]
fig2 = grouped_bar(
    edu,
    x="group_value",
    color="category",
    title="Share holding Eurosceptic views, by highest completed education",
    order=edu_order,
)
st.plotly_chart(fig2, width='stretch')

st.subheader("Euroscepticism by urban / rural residence (2023)")
ur = load("eu_attachment", "breakdown_urban_rural")
fig3 = grouped_bar(
    ur,
    x="group_value",
    color="category",
    title="Share holding Eurosceptic views, by urban / rural residence",
)
st.plotly_chart(fig3, width='stretch')

insight(
    "Eurosceptic attitudes — low trust in the EU Parliament, believing unification has already gone too "
    "far, and low emotional attachment to Europe — are more common among respondents with lower levels of "
    "education, and among rural residents compared with urban residents."
)
