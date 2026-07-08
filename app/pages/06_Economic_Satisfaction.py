import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Economic Satisfaction — ESS Ireland", page_icon="\U0001F4B6", layout="wide")

page_header(
    "Economic Satisfaction and Household Income Adequacy",
    "Satisfaction with the present state of the economy, and perceived adequacy of household income.",
)

dist = load("economic_satisfaction", "distribution")
fig_pct = trend_line(
    dist[dist["response_category"] == "Satisfied"].rename(columns={"percent": "value"}).assign(series="% Satisfied"),
    title="Share of the population satisfied with the state of the economy, 2002–2023",
)
fig_pct.update_yaxes(range=[0, 100], ticksuffix="%")
st.plotly_chart(fig_pct, width='stretch')

insight(
    "Satisfaction with the economy tracks Ireland's economic cycle closely. It collapsed from 71.6% in "
    "2004 to just 8–12% during the 2008–2012 financial crisis and recession, then recovered steadily, "
    "reaching 54.3% in 2018 and roughly 49% in 2023."
)

st.subheader("Economic satisfaction by age group (2023)")
age = load("economic_satisfaction", "breakdown_age")
age_order = ["25 and under", "26-35", "36-45", "46-55", "56-65", "66-75", "76+"]
fig2 = grouped_bar(
    age,
    x="group_value",
    color="category",
    title="Share satisfied vs. dissatisfied with the economy, by age",
    barmode="stack",
    order=age_order,
)
st.plotly_chart(fig2, width='stretch')

st.subheader("Household income adequacy by income quintile (2023)")
quint = load("economic_satisfaction", "breakdown_income_quintile")
quint_order = ["Bottom 20%", "2nd quintile", "3rd quintile", "4th quintile", "Top 20%", "All"]
cat_order = ["Living comfortably", "Coping", "Finding it difficult", "Finding it very difficult"]
fig3 = grouped_bar(
    quint,
    x="group_value",
    color="category",
    title="How people describe their household income, by income quintile",
    barmode="stack",
    order=quint_order,
)
st.plotly_chart(fig3, width='stretch')

insight(
    "Perceived income adequacy rises sharply with income: only 17% of the bottom quintile say they are "
    "'living comfortably' on their present income, compared with the large majority of the top quintile. "
    "Difficulty coping on present income is concentrated in the lowest income groups."
)
