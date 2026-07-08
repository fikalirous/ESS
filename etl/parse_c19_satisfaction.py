"""
Parse the 'C19 - Satisfaction' sheet from the ESS11 Ireland report workbook
into tidy long-format CSVs.

Structure (confirmed by manual inspection + programmatic anchor search):
Five satisfaction-with-government's-COVID-19-response questions, each an
11-point (0-10, "Extremely dissatisfied" .. "Extremely satisfied") scale,
each printed as:
  1. an OVERALL Freq/Percent/Cum distribution table (11 rows)
  2. three PER-GROUP Freq/Percent/Cum sub-tables (one per "personal C19
     experience" group) - redundant with (3), not re-emitted
  3. one wide CROSSTAB table with the same per-group breakdown as 3
     side-by-side percent columns - used as the breakdown CSV source

Unlike the Prioritisations sheet, the endpoint labels here ("Extremely
dissatisfied" / "Extremely satisfied") are NOT truncated in the overall
vertical tables, so no label repair is needed.

ESS round / year: see parse_c19_personal_experience.py docstring - the C19
module was fielded once, in ESS Round 10 (Irish fieldwork 2021/22).
"""
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ess_helpers import (
    load_ws, find_freq_anchors, extract_vertical_table,
    find_crosstab_anchors, extract_crosstab, GROUP_NAMES_C19_EXPERIENCE,
)

SRC = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish\ESS11_graphs_Ausra (version2)_20241209.xlsx"
OUT_DIR = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish\data\processed"
SHEET = "C19 - Satisfaction"
ESS_ROUND = 10
YEAR = "2021/22"

# (overall table header_row, output slug) - header rows confirmed against
# known table totals (1739/1735/1718/1704/1695) via manual cross-check
QUESTIONS = [
    (7, "government_handling"),
    (92, "health_services"),
    (181, "job_income_losses"),
    (269, "elderly_care_homes"),
    (357, "school_aged_children"),
]


def label_to_str(lbl):
    if isinstance(lbl, (int, float)):
        return str(int(lbl))
    return str(lbl).strip()


def main():
    ws = load_ws(SRC, SHEET)
    anchors = find_freq_anchors(ws)
    anchors_by_row = {r: c for (r, c) in anchors}

    for header_row, slug in QUESTIONS:
        assert header_row in anchors_by_row, f"expected Freq. header at row {header_row}"
        freq_col = anchors_by_row[header_row]
        later_anchors = [r for r in anchors_by_row if r > header_row]
        max_scan = min(later_anchors) - 1 if later_anchors else ws.max_row
        rows, total = extract_vertical_table(ws, header_row, freq_col, max_scan)
        out_rows = [(ESS_ROUND, YEAR, label_to_str(lbl), round(freq, 4), round(pct, 4), round(cum, 4))
                    for (lbl, freq, pct, cum) in rows]
        df = pd.DataFrame(out_rows, columns=["ess_round", "year", "response_category", "freq", "percent", "cum_percent"])
        out_path = os.path.join(OUT_DIR, f"c19_satisfaction__distribution_{slug}.csv")
        df.to_csv(out_path, index=False)
        print(f"\n{out_path}  ({len(df)} rows, total N={total})")
        print(df.to_string(index=False))

    # --- combined breakdown CSV (by personal C19 experience) across all 5 questions ---
    cx_anchors = find_crosstab_anchors(ws, GROUP_NAMES_C19_EXPERIENCE)
    assert len(cx_anchors) == len(QUESTIONS), f"expected {len(QUESTIONS)} crosstabs, found {len(cx_anchors)}"
    group_labels = [g.strip() for g in GROUP_NAMES_C19_EXPERIENCE]

    breakdown_rows = []
    for (header_row, group_start_col), (_, slug) in zip(cx_anchors, QUESTIONS):
        cx_rows = extract_crosstab(ws, header_row, group_start_col)
        for (lbl, v1, v2, v3) in cx_rows:
            cat = label_to_str(lbl)
            for group_label, val in zip(group_labels, (v1, v2, v3)):
                if val is None:
                    continue
                breakdown_rows.append((f"{slug}: {cat}", "c19_experience", group_label, round(float(val), 4), "percent"))

    bdf = pd.DataFrame(breakdown_rows, columns=["category", "group_type", "group_value", "value", "unit"])
    bout = os.path.join(OUT_DIR, "c19_satisfaction__breakdown_c19_experience.csv")
    bdf.to_csv(bout, index=False)
    print(f"\n{bout}  ({len(bdf)} rows)")
    print(bdf.head(15).to_string(index=False))
    print(f"  value range: {bdf['value'].min()} - {bdf['value'].max()}")


if __name__ == "__main__":
    main()
