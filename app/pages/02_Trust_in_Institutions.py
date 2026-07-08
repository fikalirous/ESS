import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.charts import grouped_bar, trend_line
from utils.components import insight, page_header
from utils.data_loader import load

st.set_page_config(page_title="Trust in Institutions — ESS Ireland", page_icon="\U0001F3DB️", layout="wide")

page_header(
    "Trust in Institutions",
    "Personal trust (0–10) in the Garda, the legal system, parliament, politicians and political parties.",
)

INSTITUTION_ORDER = ["Garda", "Legal System", "Parliament", "Political Parties", "Politicians"]

trend = load("trust_institutions", "trend")
fig = trend_line(trend, title="Mean trust in political actors and institutions, 2002–2023")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig, width='stretch')

insight(
    "Trust in the Garda remains consistently the highest and most stable of the five, with only minor "
    "declines around 2006 and after 2012. Trust in parliament, politicians and political parties fell "
    "sharply during the 2008–2012 economic crisis, reaching a low around 2012, before gradually recovering — "
    "by 2023 trust in these actors had returned to, or slightly exceeded, pre-crisis levels."
)

st.subheader("Low vs. high trust, by institution (2023)")
dist_frames = []
for slug in ["garda", "legal_system", "parliament", "political_parties", "politicians"]:
    name = slug.replace("_", " ").title().replace("Garda", "Garda")
    df = load("trust_institutions", f"distribution_{slug}")
    if df is not None:
        df = df[df["ess_round"] == 11].copy()
        df["institution"] = name
        dist_frames.append(df)
if dist_frames:
    dist_all = pd.concat(dist_frames, ignore_index=True)
    band_order = ["Lower Trust (0-4)", "Neutral answer (5)", "Higher Trust (6-10)"]
    fig_dist = grouped_bar(
        dist_all,
        x="institution",
        y="percent",
        color="response_category",
        title="Share reporting low / neutral / high trust, 2023",
        barmode="stack",
        order=INSTITUTION_ORDER,
    )
    st.plotly_chart(fig_dist, width='stretch')

insight(
    "The Garda are the most trusted institution — 69% of respondents report high trust (a score of 6–10). "
    "The legal system follows at 58%. Politicians and political parties are trusted comparatively less, "
    "with nearly half of respondents reporting low trust (a score of 0–4)."
)

st.subheader("High trust by education (2023)")
edu = load("trust_institutions", "breakdown_education")
edu_order = ["<Lower Secondary", "Lower Secondary", "Upper Secondary", "Advanced Vocational", "Tertiary"]
fig2 = grouped_bar(
    edu,
    x="group_value",
    color="category",
    title="Share reporting high trust (6–10), by highest completed education",
    order=edu_order,
)
st.plotly_chart(fig2, width='stretch')

insight(
    "Trust increases with educational attainment across every institution. Respondents with tertiary "
    "education report the greatest trust in the Garda, followed by the legal system and parliament. The "
    "widest gaps between tertiary-educated respondents and other groups appear in trust of parliament and "
    "the legal system."
)
