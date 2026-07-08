import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import diverging_ramp, horizontal_bar, horizontal_stacked_bar, ordinal_ramp
from utils.components import data_insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="COVID-19 — ESS Ireland", page_icon="\U0001F9A0", layout="wide")

page_header(
    "COVID-19",
    "A rotating ESS module fielded in round 10 (2021/22), asked as Ireland emerged from the pandemic. "
    "This topic is not covered in the published report — the charts below are a direct read of the data.",
)

tab1, tab2, tab3 = st.tabs(["Personal experience", "Policy priorities", "Satisfaction with the response"])

with tab1:
    st.markdown("**Had COVID-19?**")
    df = load("c19_personal_experience", "had_covid19").copy()
    df["response_category"] = df["response_category"].replace({
        "Yes, I tested positive for COVID-19": "Yes, tested positive",
        "Yes, I think I had COVID-19 but was not tested/did not test positive": "Think I had it, not tested",
        "No, I have not had COVID-19": "No",
    })
    fig = horizontal_bar(df, x="percent", y="response_category", title="")
    fig.update_layout(height=280)
    st.plotly_chart(fig, width='stretch')

    st.markdown("**Anyone in the household had COVID-19?**")
    df = load("c19_personal_experience", "household_covid19").copy()
    df["response_category"] = df["response_category"].replace({
        "Yes, someone living with me tested positive for COVID-19": "Yes, someone tested positive",
        "Yes, I think someone living with me had COVID-19 but they  were not tested/did no": "Think someone had it, not tested",
        "No, no one living with me had COVID-19": "No",
        "I have not lived with anyone since the start of the pandemic": "Haven't lived with anyone",
    })
    fig = horizontal_bar(df, x="percent", y="response_category", title="")
    fig.update_layout(height=280)
    st.plotly_chart(fig, width='stretch')

    st.markdown("**Pandemic-related job or income impacts**")
    impacts = load("c19_personal_experience", "pandemic_impacts")
    marked = impacts[impacts["response_category"].str.endswith(": Marked")].copy()
    marked["response_category"] = marked["response_category"].str.replace(": Marked", "", regex=False)
    marked = marked.sort_values("percent", ascending=True)
    fig = horizontal_bar(marked, x="percent", y="response_category", title="")
    st.plotly_chart(fig, width='stretch')

    data_insight(
        "Nearly half of respondents (47%) tested positive for COVID-19 at some point, and half again had "
        "someone in their household test positive. On job and income impacts, the most common single "
        "effect was being furloughed (11%), followed by reduced working hours (6%) and reduced job income "
        "(5%) — but a clear majority (59%) reported none of these pandemic-related job or income impacts."
    )

with tab2:
    st.caption(
        "Each item asks respondents to place themselves on an 11-point scale between two competing "
        "priorities during the pandemic."
    )
    priority_items = {
        "Public health vs. economic activity": (
            "health_vs_economy",
            "Prioritise public health",
            "Prioritise economic activity",
        ),
        "Monitoring the public vs. protecting privacy": (
            "privacy_vs_monitoring",
            "Monitor and track the public",
            "Maintain public privacy",
        ),
        "Following government rules vs. own decisions": (
            "rules_vs_own_decisions",
            "Follow government rules",
            "Make own decisions",
        ),
    }
    means = {}
    for label, (slug, pole_a, pole_b) in priority_items.items():
        df = load("c19_prioritisations", f"distribution_{slug}")
        means[label] = (df["percent"].reset_index(drop=True) * range(11)).sum() / 100

    choice = st.selectbox("Choose a priority", list(priority_items.keys()))
    slug, pole_a, pole_b = priority_items[choice]
    df = load("c19_prioritisations", f"distribution_{slug}")
    plot_df = df.copy()
    plot_df["position"] = range(11)
    fig = horizontal_stacked_bar(
        plot_df.assign(dummy="All respondents"),
        x="percent",
        y="dummy",
        color="response_category",
        title="",
        category_order=df["response_category"].tolist(),
        color_sequence=diverging_ramp(11),
    )
    fig.update_layout(height=220, showlegend=False)
    st.plotly_chart(fig, width='stretch')
    st.caption(f"← {pole_a}  ·  mean position on 0–10 scale: {means[choice]:.1f}  ·  {pole_b} →")

    data_insight(
        "Opinion leans toward prioritising public health over the economy (mean 3.9 of 10, where 0 = "
        "public health) and, more mildly, toward following government rules over making one's own "
        "decisions (mean 4.6). On surveillance, opinion leans more clearly toward maintaining public "
        "privacy over monitoring and tracking the public (mean 6.6, where 10 = privacy)."
    )

with tab3:
    st.caption("Satisfaction with different aspects of Ireland's pandemic response, 0 (extremely dissatisfied) to 10 (extremely satisfied).")
    sat_items = [
        ("Government's handling of the pandemic", "government_handling"),
        ("The health service", "health_services"),
        ("Support for job and income losses", "job_income_losses"),
        ("Care of the elderly in care homes", "elderly_care_homes"),
        ("Support for school-aged children", "school_aged_children"),
    ]
    mean_rows = []
    for label, slug in sat_items:
        df = load("c19_satisfaction", f"distribution_{slug}")
        mean_val = (df["percent"].reset_index(drop=True) * range(11)).sum() / 100
        mean_rows.append({"item": label, "mean_satisfaction": mean_val})
    means_df = pd.DataFrame(mean_rows).sort_values("mean_satisfaction", ascending=True)
    fig = horizontal_bar(means_df, x="mean_satisfaction", y="item", title="Mean satisfaction (0–10 scale)", y_suffix="")
    st.plotly_chart(fig, width='stretch')

    choice_label = st.selectbox("View full distribution for", [s[0] for s in sat_items])
    slug = dict(sat_items)[choice_label]
    df = load("c19_satisfaction", f"distribution_{slug}")
    fig2 = horizontal_stacked_bar(
        df.assign(dummy="All respondents"),
        x="percent",
        y="dummy",
        color="response_category",
        title="",
        category_order=df["response_category"].tolist(),
        color_sequence=ordinal_ramp(11),
    )
    fig2.update_layout(height=220, showlegend=False)
    st.plotly_chart(fig2, width='stretch')

    data_insight(
        "The government's overall handling of the pandemic (mean 6.7 of 10) and the health service (mean "
        "6.5) drew the most positive ratings. Satisfaction was markedly lower for care of the elderly in "
        "care homes (mean 4.5, the only area rated below the scale midpoint) and support for school-aged "
        "children (mean 5.5)."
    )
