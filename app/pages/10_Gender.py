import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, ordinal_ramp, stacked_percent_bar
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Gender — ESS Ireland", page_icon="⚖️", layout="wide")

page_header(
    "Gender",
    "ESS Round 11's special module: 'Gender in Contemporary Europe: Rethinking Equality and the Backlash.'",
)

tab1, tab2, tab3 = st.tabs(["Experiences of unfair treatment", "Perceptions of fairness", "Attitudes to gender equality"])

with tab1:
    st.subheader("Unfairly treated in hiring, pay or promotion because of gender")
    df = load("gender", "unfair_hiring")
    order = ["Yes, once", "Yes, more than once", "No", "Have never had job or applied for a job"]
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=["Male", "Female"])
    st.plotly_chart(fig, width='stretch')
    insight(
        "Almost one in five women (18%, combining 'once' and 'more than once') report having experienced "
        "unfair treatment in hiring, pay or promotion because of their gender. Among men the corresponding "
        "share is substantially lower, at around 8% — a pronounced gender gap in reported workplace "
        "discrimination."
    )

    st.subheader("Unfairly treated by the police because of gender")
    df = load("gender", "unfair_police")
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=["Male", "Female"])
    st.plotly_chart(fig, width='stretch')
    insight(
        "Gender-based unfair treatment by the police is rare for both women (4%) and men (6%). The large "
        "majority of both women (87%) and men (88%) report no such experience — a much lower prevalence "
        "than in workplace settings."
    )

with tab2:
    st.subheader("Gender equality when seeking medical treatment")
    df = load("gender", "medical_equality")
    order = ["Women and men are treated equally fairly", "Women are treated less fairly than men", "Men are treated less fairly than women"]
    fig = grouped_bar(df, x="group_value", color="category", title="", barmode="stack", order=["Male", "Female"])
    st.plotly_chart(fig, width='stretch')
    insight(
        "A clear majority believe women and men are treated equally fairly when seeking medical care, "
        "though more so among men (82%) than women (76%). 20% of women believe women are treated less "
        "fairly than men in medical settings, compared with 12% of men who hold that view."
    )

    fair_hire = load("gender", "fair_hiring_perception")
    if fair_hire is not None:
        st.subheader("Perceived fairness in hiring by gender")
        fig = grouped_bar(fair_hire, x="group_value", color="category", title="", barmode="stack", order=["Male", "Female"])
        st.plotly_chart(fig, width='stretch')
        insight(
            "Women are substantially more likely than men to say women are treated less fairly than men in "
            "hiring: 53% of women hold this view, compared with 38% of men — the largest gender gap in "
            "perception among the fairness measures in this module."
        )

with tab3:
    st.caption("Distributions shown on their original response scale; higher/greener = more positive toward gender equality.")
    options = {
        "Equal participation in paid work is good for family life (0–6 scale)": (
            "paid_work_attitude",
            ["0 - Very bad for family life", "1", "2", "3", "4", "5", "6 - Very good for family life"],
            "77% of both women and men rate equal participation in paid work as good for family life "
            "(scoring 4 or higher). 'Very good for family life' is the single most common response for "
            "both genders (35% of women, 34% of men).",
        ),
        "Equal political leadership is good for politics (0–6 scale)": (
            "political_leadership_attitude",
            ["0 - Very bad for politics", "1", "2", "3", "4", "5", "6 - Very good for politics"],
            "A clear majority of both genders see gender-balanced political leadership as good for "
            "politics, with women expressing stronger support (85% score 4+) than men (77%). 'Very good for "
            "politics' is the most common response for both, selected by 48% of women and 39% of men.",
        ),
        "Equal business leadership is good for business (0–6 scale)": (
            "business_leadership_attitude",
            ["0 - Very bad for businesses", "1", "2", "3", "4", "5", "6 - Very good for businesses"],
            "83% of men and 88% of women evaluate gender-balanced leadership as good for business "
            "(scoring 4+). 'Very good for businesses' is the top response for both, chosen by 52% of women "
            "and 40% of men.",
        ),
        "Equal pay is good for the economy (0–6 scale)": (
            "equal_pay_attitude",
            ["0 - Very bad for the economy", "1", "2", "3", "4", "5", "6 - Very good for the economy"],
            "Near-universal support for equal pay: 94% of women and 87% of men evaluate it as good for the "
            "economy (scoring 4+). 'Very good for the economy' is the top response for both, selected by "
            "59% of women and 50% of men.",
        ),
        "Support for equal parental leave requirement (favour–against scale)": (
            "parental_leave_attitude",
            ["Strongly in favour", "Somewhat in favour", "Neither in favour nor against", "Somewhat against", "Strongly against"],
            "Broad support for requiring both parents to take equal paid leave: 73% of women and 63% of men "
            "are in favour (combining 'strongly' and 'somewhat'). 'Strongly in favour' is chosen by 41% of "
            "women versus 31% of men — support is consistently stronger among women.",
        ),
    }
    choice = st.selectbox("Choose an attitude statement", list(options.keys()))
    slug, cat_order, text = options[choice]
    df = load("gender", slug)
    fig = stacked_percent_bar(
        df,
        x="group_value",
        color="category",
        title="",
        order=["Male", "Female"],
        category_order=cat_order,
        color_sequence=ordinal_ramp(len(cat_order)),
    )
    st.plotly_chart(fig, width='stretch')
    insight(text)
