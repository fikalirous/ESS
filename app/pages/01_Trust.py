import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Trust — ESS Ireland", page_icon="\U0001F91D", layout="wide")

page_header(
    "Trust in Others",
    "Generally speaking, would you say that most people can be trusted, or that you can't be too careful?",
)

trend = load("trust_others", "trend")
fig = trend_line(trend, title="Average trust in other people, 2002–2023", y_suffix="")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig, width='stretch')

insight(
    "Trust in others ranged from 5.19 (2012) to 5.81 (2004). After the 2004 peak, trust fell through the "
    "2008–2012 economic crisis and recession, then climbed back and stabilised around 5.5 between 2016 and "
    "2021/22, with a small dip in 2023."
)

st.subheader("Trust by education (2023)")
edu = load("trust_others", "breakdown_education")
edu_order = ["<Lower Secondary", "Lower Secondary", "Upper Secondary", "Advanced Vocational", "Tertiary"]
band_order = ["Lower Trust (0-4)", "Neutral answer (5)", "Higher Trust (6-10)"]
fig2 = grouped_bar(
    edu,
    x="group_value",
    color="category",
    title="Trust band by highest completed education",
    barmode="stack",
    order=edu_order,
)
st.plotly_chart(fig2, width='stretch')

insight(
    "Respondents with tertiary education report the highest trust: 66% place their trust between 6 and 10 "
    "on the 11-point scale. Trust among those with advanced vocational degrees sits between secondary and "
    "tertiary levels, while the various secondary-school groups show little variation from one another."
)
