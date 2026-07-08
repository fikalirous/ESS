import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))

st.set_page_config(
    page_title="Irish Social Attitudes 2023 — ESS Round 11",
    page_icon="\U0001F1EE\U0001F1EA",
    layout="wide",
)

st.title("Irish Social Attitudes: 2023")
st.caption("Interactive exploration of Round 11 of the European Social Survey (ESS) in Ireland")

st.markdown(
    """
This dashboard turns the University College Dublin *Irish Social Attitudes: 2023* report and its
underlying data into an interactive companion. Every page tracks how Irish public opinion has moved
across ESS rounds 1–11 (2002–2023), and breaks the latest wave down by education, age, gender,
employment, income and urban/rural residence where the data allows it.

Use the sidebar to move between topics.
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Sample issued", "3,930")
col2.metric("Completed interviews", "≈2,075")
col3.metric("Response rate", "52.8%")
col4.metric("Fieldwork", "Jun 2023 – Jan 2024")

st.divider()

st.subheader("What's covered")
topics = [
    ("Trust", "Interpersonal trust, 2002–2023, and how it varies by education."),
    ("Trust in Institutions", "Trust in the Garda, legal system, parliament, politicians and political parties."),
    ("Health & Health Services", "Self-reported health, healthcare satisfaction, wellbeing, and accommodation problems."),
    ("Europe", "Trust in the EU Parliament, support for unification, and emotional attachment to Europe."),
    ("Life Satisfaction & Happiness", "Life satisfaction and happiness trends, and satisfaction by employment status."),
    ("Economic Satisfaction", "Satisfaction with the economy and household income adequacy."),
    ("Immigration", "Perceived impact of immigration on the economy, culture and quality of life."),
    ("Religion", "Religious belonging over time and across demographic groups."),
    ("Climate Change", "Belief in the effectiveness of individual and government climate action."),
    ("Gender", "The ESS11 gender module — workplace discrimination and attitudes to equality."),
    ("COVID-19", "Personal experience, policy priorities, and satisfaction during the pandemic."),
    ("Precarity", "Economic and job security indicators."),
]
grid = st.columns(3)
for i, (name, desc) in enumerate(topics):
    with grid[i % 3]:
        st.markdown(f"**{name}**")
        st.caption(desc)

st.divider()

with st.expander("About the survey"):
    st.markdown(
        """
The European Social Survey (ESS) is a cross-national survey run every two years across Europe.
Round 11 fieldwork in Ireland ran from **27 June 2023 to 3 January 2024**, carried out face-to-face
(CAPI/CAMI) by 88 trained interviewers. A three-stage probability sample was drawn from the
Geodirectory address database: 655 electoral-division clusters were selected across 17 urban/rural
strata, 6 addresses per cluster, and one individual per address via the last-birthday method.
Of 3,930 issued sample units, 52.8% responded, yielding roughly 2,075 completed interviews.

Report authors: Micheál L. Collins, Mathew J. Creighton, Ebru Işıklı, Ausra Cizauskaite, Sarah Carol
and Dorren McMahon — UCD Geary Institute for Public Policy.

Source data: [ESS Round 11 datafile](https://ess.sikt.no/en/datafile/242aaa39-3bbb-40f5-98bf-bfb1ce53d8ef)
"""
    )

st.caption("Built with Streamlit · Data: European Social Survey Round 11, Ireland")
