import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Religion — ESS Ireland", page_icon="\U0001F54A️", layout="wide")

page_header(
    "Religion",
    "Do you consider yourself as belonging to any particular religion or denomination?",
)

trend = load("religion", "trend")
fig = trend_line(trend, title="Share belonging to a religion, 2002–2023")
fig.update_yaxes(range=[0, 100], ticksuffix="%")
st.plotly_chart(fig, width='stretch')

insight(
    "68% of respondents in Ireland belonged to a religion in 2023, slightly more than in previous years. "
    "This reverses — though does not fully undo — a steady decline of more than a decade from the peak of "
    "86% in 2004. The large majority of those with a religious affiliation are Roman Catholic."
)

st.subheader("Religious belonging by demographic group (2023)")
tab1, tab2, tab3, tab4 = st.tabs(["By gender", "By age", "By education", "By location"])

with tab1:
    df = load("religion", "breakdown_gender")
    fig_g = grouped_bar(df, x="group_value", color="category", title="Belonging to a religion, by gender", barmode="stack")
    st.plotly_chart(fig_g, width='stretch')

with tab2:
    df = load("religion", "breakdown_age")
    order = ["25 and under", "26-35", "36-45", "46-55", "56-65", "66-75", "76 plus"]
    fig_a = grouped_bar(df, x="group_value", color="category", title="Belonging to a religion, by age", barmode="stack", order=order)
    st.plotly_chart(fig_a, width='stretch')

with tab3:
    df = load("religion", "breakdown_education")
    order = ["Less than lower secondary", "Lower secondary", "Upper secondary", "Advanced vocational", "Tertiary education"]
    fig_e = grouped_bar(df, x="group_value", color="category", title="Belonging to a religion, by education", barmode="stack", order=order)
    st.plotly_chart(fig_e, width='stretch')

with tab4:
    df = load("religion", "breakdown_urban_rural")
    fig_u = grouped_bar(df, x="group_value", color="category", title="Belonging to a religion, by urban / rural residence", barmode="stack")
    st.plotly_chart(fig_u, width='stretch')

insight(
    "Religious affiliation is more common among women (72%) than men (64%), rises steadily with age — "
    "from 56% among those 25 and under to 86% among those 76 and older — and is more common in rural areas "
    "(72%) than urban areas (64%). The youngest age group shows the sharpest recent change: 56% now report "
    "belonging to a religion, up markedly from 49.5% in the previous round."
)
