"""
Parse the 'C19 - Personal experience' sheet from the ESS11 Ireland report
workbook into tidy long-format CSVs.

The sheet has no explicit ESS-round marker of its own, but the C19
(COVID-19) module was only fielded once in the Irish ESS series: as a
rotating module in ESS Round 10 (Irish fieldwork 2021/22 - delayed by the
pandemic, run alongside/just before the Round 11 2023 fieldwork covered by
the rest of this workbook). This is corroborated by the accompanying PDF
report (`ESS11 Public Report.docx.pdf`), which explicitly attributes its
other rotating-module content ("Inequalities in Health") to "round 10", and
separately refers to the pre-2023 wave as "2021/2". All three C19 sheets in
this workbook are therefore tagged ess_round=10, year="2021/22" throughout.
See NOTES.md for the full judgment-call writeup.
"""
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ess_helpers import load_ws, find_freq_anchors, find_captions, nearest_caption_text, extract_vertical_table

SRC = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish\ESS11_graphs_Ausra (version2)_20241209.xlsx"
OUT_DIR = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish\data\processed"
SHEET = "C19 - Personal experience"
ESS_ROUND = 10
YEAR = "2021/22"

IMPACT_ITEMS = {
    "Figure X: Percent who were made redundant/lost their job": "Made redundant/lost job",
    "Figure X: Percent whose income from job was reduced": "Income from job reduced",
    "Figure X: Percent whose working hours were reduced": "Working hours reduced",
    "Figure X: Percent who were furloughed": "Furloughed",
    "Figure X: Percent who were forced to take unpaid leave/holiday": "Forced to take unpaid leave/holiday",
    "Figure X: None of these": "None of these (no pandemic-related job/income impact)",
}


def main():
    ws = load_ws(SRC, SHEET)
    anchors = find_freq_anchors(ws)
    caps = find_captions(ws)

    tables = []
    for i, (r, c) in enumerate(anchors):
        max_scan = anchors[i + 1][0] - 1 if i + 1 < len(anchors) else ws.max_row
        rows, total = extract_vertical_table(ws, r, c, max_scan)
        cap = nearest_caption_text(r, caps)
        tables.append({"header_row": r, "caption": cap, "rows": rows, "total": total})

    # --- Table 1: "Respondent had COVID-19" ---
    t1 = next(t for t in tables if "Percent Reported Having COVID-19" in t["caption"])
    df1 = pd.DataFrame(
        [(ESS_ROUND, YEAR, lbl, round(freq, 4), round(pct, 4), round(cum, 4))
         for (lbl, freq, pct, cum) in t1["rows"]],
        columns=["ess_round", "year", "response_category", "freq", "percent", "cum_percent"],
    )
    out1 = os.path.join(OUT_DIR, "c19_personal_experience__distribution_had_covid19.csv")
    df1.to_csv(out1, index=False)

    # --- Table 2: "Someone at home had COVID-19" ---
    t2 = next(t for t in tables if "Someone at Home who had COVID-19" in t["caption"])
    df2 = pd.DataFrame(
        [(ESS_ROUND, YEAR, lbl, round(freq, 4), round(pct, 4), round(cum, 4))
         for (lbl, freq, pct, cum) in t2["rows"]],
        columns=["ess_round", "year", "response_category", "freq", "percent", "cum_percent"],
    )
    out2 = os.path.join(OUT_DIR, "c19_personal_experience__distribution_household_covid19.csv")
    df2.to_csv(out2, index=False)

    # --- Tables 3-8: pandemic job/income impact checklist items (each a binary Marked/Not-marked table) ---
    impact_rows = []
    for t in tables:
        if t["caption"] in IMPACT_ITEMS:
            item_label = IMPACT_ITEMS[t["caption"]]
            for (lbl, freq, pct, cum) in t["rows"]:
                impact_rows.append((ESS_ROUND, YEAR, f"{item_label}: {lbl}", round(freq, 4), round(pct, 4), round(cum, 4)))
    df3 = pd.DataFrame(impact_rows, columns=["ess_round", "year", "response_category", "freq", "percent", "cum_percent"])
    out3 = os.path.join(OUT_DIR, "c19_personal_experience__distribution_pandemic_impacts.csv")
    df3.to_csv(out3, index=False)

    print("=== C19 - Personal experience ETL summary ===")
    for path, df in [(out1, df1), (out2, df2), (out3, df3)]:
        print(f"\n{path}  ({len(df)} rows)")
        print(df.head(10).to_string(index=False))
        if "percent" in df.columns:
            print(f"  percent range: {df['percent'].min()} - {df['percent'].max()}")


if __name__ == "__main__":
    main()
