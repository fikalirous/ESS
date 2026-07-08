"""
ETL parser for the 'Immigration' sheet of
ESS11_graphs_Ausra (version2)_20241209.xlsx

Produces tidy CSVs in data/processed/:
  - immigration__trend.csv                    (ESS round 1-11 mean scores 0-10, 3 series: Economy/Culture/Place to live)
  - immigration__breakdown_education.csv      (Figure 7.2 style % positive view by education, 3 series)
  - immigration__breakdown_education_detail.csv (Negative/Positive view % by education, 3 series)
  - immigration__breakdown_employment.csv     (Figure 7.3 style % positive view by employment status, 3 series)
  - immigration__breakdown_employment_detail.csv (Negative/Positive view % by employment status, 3 series)

Note: the per-round "Variable/Obs/Weight/Mean/Std.dev/Min/Max" stat blocks (rows 4-97,
variables imbgeco/imueclt/imwbcnt) are redundant with the compact trend table at rows 3-7
(same Mean values) and are therefore not separately extracted -- the trend CSV below is
built from the compact table.

Run standalone: python parse_immigration.py
"""
import os
import openpyxl
import pandas as pd

BASE_DIR = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish"
XLSX_PATH = os.path.join(BASE_DIR, "ESS11_graphs_Ausra (version2)_20241209.xlsx")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")
SHEET_NAME = "Immigration"

os.makedirs(OUT_DIR, exist_ok=True)


def load_ws():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    return wb[SHEET_NAME]


def cell(ws, r, c):
    return ws.cell(row=r, column=c).value


def clean_num(v):
    if v is None or v == "":
        return None
    try:
        return round(float(v), 4)
    except (ValueError, TypeError):
        return None


def year_to_str(v):
    if v is None or v == "":
        return None
    if isinstance(v, str):
        return v.strip()
    return str(int(v))


# ---------------------------------------------------------------------------
# Trend: rows 3-7, cols I(label)/J..T(round1-11 values); round row=3, year row=4
# ---------------------------------------------------------------------------
def parse_trend(ws):
    round_row = 3
    year_row = 4
    series_rows = {5: "Economy", 6: "Culture", 7: "Place to live"}
    rows = []
    for c in range(10, 21):  # J(10) .. T(20)
        ess_round = cell(ws, round_row, c)
        if ess_round is None:
            continue
        ess_round = int(ess_round)
        year_s = year_to_str(cell(ws, year_row, c))
        for r, series_name in series_rows.items():
            val = clean_num(cell(ws, r, c))
            if val is None:
                continue
            rows.append({
                "ess_round": ess_round, "year": year_s,
                "series": series_name, "value": val,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Breakdown by education - summary % positive view (Figure 7.2)
# cols P(label) Q(Economy) R(Culture) S(Place to live), rows 102-106
# ---------------------------------------------------------------------------
def parse_breakdown_education_summary(ws):
    label_col = 16  # P
    metric_cols = {17: "Economy", 18: "Culture", 19: "Place to live"}  # Q, R, S
    data_rows = [102, 103, 104, 105, 106]
    rows = []
    for r in data_rows:
        group_value = cell(ws, r, label_col)
        if group_value is None:
            continue
        group_value = str(group_value).strip()
        for col, metric in metric_cols.items():
            val = clean_num(cell(ws, r, col))
            if val is None:
                continue
            rows.append({
                "category": metric,
                "group_type": "education",
                "group_value": group_value,
                "value": val,
                "unit": "percent",
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Breakdown by education - detail Negative/Positive view % per metric
# blocks: title_row -> header=title+1, data=[title+3, title+4]
# columns: economy A/B/C/D, culture F/G/H/I, placetolive K/L/M/N
# ---------------------------------------------------------------------------
def parse_breakdown_education_detail(ws):
    title_rows = [102, 110, 118, 126, 134]
    label_col = 1  # A holds the education-level title
    metric_specs = [
        ("Economy", 1, 2, 3, 4),         # A,B,C,D
        ("Culture", 6, 7, 8, 9),         # F,G,H,I
        ("Place to live", 11, 12, 13, 14),  # K,L,M,N
    ]
    rows = []
    for title_row in title_rows:
        group_value = cell(ws, title_row, label_col)
        group_value = str(group_value).strip() if group_value else None
        data_rows = [title_row + 3, title_row + 4]
        for metric, lab_c, freq_c, pct_c, cum_c in metric_specs:
            for r in data_rows:
                cat_label = cell(ws, r, lab_c)
                if cat_label is None or str(cat_label).strip() == "":
                    continue
                pct = clean_num(cell(ws, r, pct_c))
                if pct is None:
                    continue
                rows.append({
                    "category": f"{metric} - {str(cat_label).strip()}",
                    "group_type": "education",
                    "group_value": group_value,
                    "value": pct,
                    "unit": "percent",
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Breakdown by employment - summary % positive view (Figure 7.3)
# row143 header G/H/I = Economy/Culture/Place to live; data rows 144 (In paid work), 145 (Unemployed)
# ---------------------------------------------------------------------------
def parse_breakdown_employment_summary(ws):
    metric_cols = {7: "Economy", 8: "Culture", 9: "Place to live"}  # G, H, I
    data = [(144, "In paid work"), (145, "Unemployed")]
    label_col = 6  # F
    rows = []
    for r, _expected_label in data:
        group_value = cell(ws, r, label_col)
        group_value = str(group_value).strip() if group_value else _expected_label
        for col, metric in metric_cols.items():
            val = clean_num(cell(ws, r, col))
            if val is None:
                continue
            rows.append({
                "category": metric,
                "group_type": "employment",
                "group_value": group_value,
                "value": val,
                "unit": "percent",
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Breakdown by employment - detail Negative/Positive % per metric
# Each metric has its own pair of blocks (In paid work, Unemployed), single column set A/B/C/D
# ---------------------------------------------------------------------------
def parse_breakdown_employment_detail(ws):
    blocks = [
        ("Economy", 143, "In paid work"),
        ("Economy", 151, "Unemployed"),
        ("Culture", 159, "In paid work"),
        ("Culture", 167, "Unemployed"),
        ("Place to live", 175, "In paid work"),
        ("Place to live", 183, "Unemployed"),
    ]
    label_col, freq_c, pct_c, cum_c = 1, 2, 3, 4  # A, B, C, D
    rows = []
    for metric, title_row, group_value in blocks:
        data_rows = [title_row + 3, title_row + 4]
        for r in data_rows:
            cat_label = cell(ws, r, label_col)
            if cat_label is None or str(cat_label).strip() == "":
                continue
            pct = clean_num(cell(ws, r, pct_c))
            if pct is None:
                continue
            rows.append({
                "category": f"{metric} - {str(cat_label).strip()}",
                "group_type": "employment",
                "group_value": group_value,
                "value": pct,
                "unit": "percent",
            })
    return pd.DataFrame(rows)


def main():
    ws = load_ws()

    outputs = {
        "immigration__trend.csv": parse_trend(ws),
        "immigration__breakdown_education.csv": parse_breakdown_education_summary(ws),
        "immigration__breakdown_education_detail.csv": parse_breakdown_education_detail(ws),
        "immigration__breakdown_employment.csv": parse_breakdown_employment_summary(ws),
        "immigration__breakdown_employment_detail.csv": parse_breakdown_employment_detail(ws),
    }

    print(f"=== {SHEET_NAME} ===")
    for fname, df in outputs.items():
        out_path = os.path.join(OUT_DIR, fname)
        df.to_csv(out_path, index=False)
        print(f"\n--> {fname}: {len(df)} rows")
        print(df.head(6).to_string(index=False))
        if "value" in df.columns:
            vmin, vmax = df["value"].min(), df["value"].max()
            print(f"    value range: [{vmin}, {vmax}]")

    print("\nDone. Files written to:", OUT_DIR)


if __name__ == "__main__":
    main()
