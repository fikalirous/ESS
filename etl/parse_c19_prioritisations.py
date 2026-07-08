"""
Parse the 'C19 - Prioritisations' sheet from the ESS11 Ireland report
workbook into tidy long-format CSVs.

Structure (confirmed by manual inspection + programmatic anchor search):
Three attitude questions, each an 11-point (0-10) scale, each printed as:
  1. an OVERALL Freq/Percent/Cum distribution table (11 rows: 2 text
     endpoints + 9 bare numeric midpoints 1-9)
  2. three PER-GROUP Freq/Percent/Cum sub-tables, one for each of the 3
     "personal C19 experience" groups (tested positive / think had it /
     never had it) - these are redundant with (3) below, so not re-emitted
  3. one wide CROSSTAB table restating the same per-group breakdown as
     3 side-by-side percent columns - used as the breakdown CSV source
     since it's the more compact/complete representation

The OVERALL tables have a data-entry quirk: the two text endpoint labels
(value 0 and value 10) are truncated to ~40 characters in the vertical
table's label column (e.g. "Much more important to prioritise publi"),
while the identical labels are NOT truncated in the crosstab table's label
column. We use the crosstab's untruncated text as the canonical label.

ESS round / year: see parse_c19_personal_experience.py docstring - the C19
module was fielded once, in ESS Round 10 (Irish fieldwork 2021/22).
"""
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ess_helpers import (
    load_ws, find_freq_anchors, find_captions, nearest_caption_text,
    extract_vertical_table, find_crosstab_anchors, extract_crosstab,
    GROUP_NAMES_C19_EXPERIENCE,
)

SRC = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish\ESS11_graphs_Ausra (version2)_20241209.xlsx"
OUT_DIR = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish\data\processed"
SHEET = "C19 - Prioritisations"
ESS_ROUND = 10
YEAR = "2021/22"

# (overall table header_row, output slug, endpoint0 text, endpoint10 text)
QUESTIONS = [
    (7, "health_vs_economy",
     "Much more important to prioritise public health",
     "Much more important to prioritise economic activity"),
    (90, "privacy_vs_monitoring",
     "Much more important to monitor and track the public",
     "Much more important to maintain public privacy"),
    (172, "rules_vs_own_decisions",
     "Much more important to follow government rules",
     "Much more important to make your own decisions"),
]


def main():
    ws = load_ws(SRC, SHEET)
    anchors = find_freq_anchors(ws)
    anchors_by_row = {r: c for (r, c) in anchors}

    # --- 3 overall distribution CSVs ---
    for header_row, slug, endpoint0, endpoint10 in QUESTIONS:
        assert header_row in anchors_by_row, f"expected Freq. header at row {header_row}"
        freq_col = anchors_by_row[header_row]
        # bound the scan to just before the next known anchor
        later_anchors = [r for r in anchors_by_row if r > header_row]
        max_scan = min(later_anchors) - 1 if later_anchors else ws.max_row
        rows, total = extract_vertical_table(ws, header_row, freq_col, max_scan)

        out_rows = []
        for (lbl, freq, pct, cum) in rows:
            if isinstance(lbl, (int, float)):
                cat = str(int(lbl))
            else:
                s = str(lbl).strip()
                # repair truncated endpoint text (only ever the first or last row)
                cat = endpoint0 if s == rows[0][0] and not isinstance(rows[0][0], (int, float)) else s
                if lbl == rows[-1][0] and not isinstance(rows[-1][0], (int, float)):
                    cat = endpoint10
            out_rows.append((ESS_ROUND, YEAR, cat, round(freq, 4), round(pct, 4), round(cum, 4)))
        df = pd.DataFrame(out_rows, columns=["ess_round", "year", "response_category", "freq", "percent", "cum_percent"])
        out_path = os.path.join(OUT_DIR, f"c19_prioritisations__distribution_{slug}.csv")
        df.to_csv(out_path, index=False)
        print(f"\n{out_path}  ({len(df)} rows, total N={total})")
        print(df.to_string(index=False))

    # --- 1 combined breakdown CSV (by personal C19 experience) across all 3 questions ---
    cx_anchors = find_crosstab_anchors(ws, GROUP_NAMES_C19_EXPERIENCE)
    group_labels = [g.strip() for g in GROUP_NAMES_C19_EXPERIENCE]
    breakdown_rows = []
    for (header_row, group_start_col), (q_header_row, slug, endpoint0, endpoint10) in zip(cx_anchors, QUESTIONS):
        cx_rows = extract_crosstab(ws, header_row, group_start_col)
        for i, (lbl, v1, v2, v3) in enumerate(cx_rows):
            if isinstance(lbl, (int, float)):
                cat = str(int(lbl))
            else:
                cat = endpoint0 if i == 0 else (endpoint10 if i == len(cx_rows) - 1 else str(lbl).strip())
            for group_label, val in zip(group_labels, (v1, v2, v3)):
                if val is None:
                    continue
                breakdown_rows.append((f"{slug}: {cat}", "c19_experience", group_label, round(float(val), 4), "percent"))

    bdf = pd.DataFrame(breakdown_rows, columns=["category", "group_type", "group_value", "value", "unit"])
    bout = os.path.join(OUT_DIR, "c19_prioritisations__breakdown_c19_experience.csv")
    bdf.to_csv(bout, index=False)
    print(f"\n{bout}  ({len(bdf)} rows)")
    print(bdf.head(15).to_string(index=False))
    print(f"  value range: {bdf['value'].min()} - {bdf['value'].max()}")


if __name__ == "__main__":
    main()
