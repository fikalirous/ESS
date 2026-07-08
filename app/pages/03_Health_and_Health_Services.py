import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, horizontal_bar, horizontal_stacked_bar, ordinal_ramp, stacked_percent_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Health & Health Services — ESS Ireland", page_icon="\U0001FA7A", layout="wide")

page_header(
    "Health and Health Services",
    "Self-reported health, satisfaction with health services, and related wellbeing indicators.",
)

HEALTH_ORDER = ["Very good", "Good", "Fair/bad/very bad"]

dist = load("health", "distribution_selfreported_health")
fig = stacked_percent_bar(
    dist,
    x="year",
    y="percent",
    color="response_category",
    title="Self-reported health, 2002–2023",
    category_order=HEALTH_ORDER,
    color_sequence=ordinal_ramp(3)[::-1],
)
fig.update_xaxes(type="category")
st.plotly_chart(fig, width='stretch')

insight(
    "The share reporting 'very good' health has drifted down over the two decades, from 44% in 2002 to "
    "37% in 2023, with year-to-year fluctuation rather than a smooth trend. The share reporting poorer "
    "health (fair, bad or very bad) has correspondingly edged up, from 14% in 2002 to 19% in 2023."
)

st.subheader("Self-reported health, by employment status and education (2023)")
emp_edu = load("health", "employment_education")
tab1, tab2 = st.tabs(["By employment status", "By education"])
with tab1:
    df = emp_edu[emp_edu["group_type"] == "employment"]
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=["In paid work", "Unemployed, looking for job"])
    st.plotly_chart(fig, width='stretch')
with tab2:
    df = emp_edu[emp_edu["group_type"] == "education"]
    order = ["< Lower Secondary", "Lower Secondary", "Upper Secondary", "Advanced Vocational", "Tertiary"]
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=order)
    st.plotly_chart(fig, width='stretch')

insight(
    "Self-reported health is strongly patterned by both employment and education. Those in paid work are "
    "far more likely to report very good or good health (91% combined) than those unemployed and looking "
    "for work (82% combined). Very good health rises steadily with education, from 22% among those with "
    "less than lower-secondary education to 47% among those with tertiary education."
)

st.subheader("Good health, by income decile (2023)")
income = load("health", "income_decile")
health_income = income[income["category"].isin(["Not good health", "Good health"])]
decile_order = ["Bottom", "2", "3", "4", "5", "6", "7", "8", "9", "Top"]
fig = grouped_bar(health_income, x="group_value", color="category", title="", barmode="stack", order=decile_order)
st.plotly_chart(fig, width='stretch')

insight(
    "Good health rises sharply with household income: 60% of the bottom income decile report good health, "
    "compared with 87–93% among the top three deciles — a gap of roughly 30 percentage points between the "
    "poorest and richest respondents."
)

st.subheader("Happiness, by income decile (2023)")
happy_income = income[income["category"].isin(["Happy", "Unhappy"])]
fig = grouped_bar(happy_income, x="group_value", color="category", title="", barmode="stack", order=decile_order)
st.plotly_chart(fig, width='stretch')

insight(
    "Happiness follows a similar, if less steep, income gradient to health: 80% of the bottom income "
    "decile report being happy, rising to well above 90% among the upper-middle and top deciles."
)

st.subheader("Very good health and satisfaction with the health care system, by age (2023)")
age = load("health", "age")
tab1, tab2 = st.tabs(["Self-rated health", "Healthcare satisfaction"])
age_order = ["25 and under", "26-35", "36-45", "46-55", "56-65", "66-75", "76 plus"]
with tab1:
    df = age[age["category"].str.contains("self-rated health")]
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=age_order)
    st.plotly_chart(fig, width='stretch')
with tab2:
    df = age[age["category"].str.contains("healthcare system")]
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=age_order)
    st.plotly_chart(fig, width='stretch')

insight(
    "Very good self-rated health declines steadily with age, from 62% among those 25 and under to 17% "
    "among those 76 and older. Satisfaction with the healthcare system follows a U-shape instead: highest "
    "among the youngest (46%) and oldest (55%) age groups, and lowest among those 36–55 (30–31%)."
)

st.divider()
st.subheader("Health inequalities module")
st.caption("From the ESS rotating module on inequalities in health (2023).")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Health problems reported in the last 12 months**")
    problems = load("health_inequalities", "health_problems_12m")
    problems = problems[problems["response_category"] != "None of these"].sort_values("percent", ascending=True)
    fig = horizontal_bar(problems, x="percent", y="response_category", title="")
    st.plotly_chart(fig, width='stretch')
    st.caption("52% of respondents reported none of these conditions (not shown above).")

with col2:
    st.markdown("**Problems with accommodation**")
    accom = load("health_inequalities", "accommodation_problems").sort_values("percent", ascending=True)
    fig = horizontal_bar(accom, x="percent", y="response_category", title="")
    st.plotly_chart(fig, width='stretch')

insight(
    "Back or neck pain (18%) and muscular or joint pain (12–14%) are the most commonly reported health "
    "problems. On accommodation, mould/rot and damp/leaks are the most common issues (6–7% of "
    "households), while more severe deprivation markers like lacking an indoor flushing toilet (1.4%) are "
    "rare."
)

unable = load("health_inequalities", "unable_medical_treatment")
pct_yes = unable.loc[unable["response_category"] == "Yes", "percent"].iloc[0]
st.metric("Unable to get needed medical consultation or treatment in the last 12 months", f"{pct_yes:.1f}%")

st.markdown("**Feelings in the past week**")
feelings = load("health_inequalities", "feelings_past_week")
feelings = feelings[feelings["group_type"] == "feeling_item"]
freq_order = ["None or almost none of the time", "Some of the time", "Most of the time", "All or almost all of the time"]
item_order = [
    "Felt depressed", "Felt everything did as effort", "Sleep was restless", "Were happy",
    "Felt lonely", "Enjoyed life", "Felt sad", "Could not get going",
]
fig = horizontal_stacked_bar(
    feelings,
    y="group_value",
    color="category",
    title="",
    order=item_order,
    category_order=freq_order,
    color_sequence=ordinal_ramp(4),
)
st.plotly_chart(fig, width='stretch')

insight(
    "13.5% of respondents were unable to get a medical consultation or treatment they needed at some "
    "point in the last 12 months. On the weekly wellbeing battery, positively-framed items dominate: 82% "
    "felt happy and 82% enjoyed life most or all of the time, while negative feelings were comparatively "
    "rare — only 3% felt depressed most or all of the time, though restless sleep was more common, "
    "affecting 14% most or all of the time."
)
