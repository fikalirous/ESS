import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Climate Change — ESS Ireland", page_icon="\U0001F30D", layout="wide")

page_header(
    "Climate Change",
    "Perceptions of the likely effectiveness of individual and government action on climate change.",
)

trend = load("climate_change", "trend")
fig = trend_line(trend, title="Perceptions of climate change action, 2016–2023 (0–10 scale)")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig, width='stretch')

insight(
    "Respondents in 2023 were most positive about the potential effectiveness of collective action: if "
    "large numbers of people limited their energy use, climate change could be reduced (mean score 6.1, "
    "a slight increase on previous rounds). They were far less confident that people actually will limit "
    "their energy use (mean 4.5, up from 4.3 in 2016), or that governments in enough countries will take "
    "sufficient action (mean 5.0, up from 4.7 in 2016). In short: people believe individual behaviour "
    "change could help, but have comparatively low confidence that either individuals or governments will "
    "follow through."
)
