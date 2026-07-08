"""
ETL parser for the 'Europ Unif and Attach to Europ' sheet of
ESS11_graphs_Ausra (version2)_20241209.xlsx

Produces tidy CSVs in data/processed/:
  - eu_attachment__distribution.csv          (ESS9 2018 & ESS11 2023 Freq/Percent/Cum, 3 variables)
  - eu_attachment__trend.csv                  (ESS round 1-11 mean scores, 2 series)
  - eu_attachment__breakdown_education.csv    (Figure 4.3 style Euroscepticism % by education)
  - eu_attachment__breakdown_education_detail.csv (full Sceptical/Neutral/Pro % by education, 3 vars)
  - eu_attachment__breakdown_urban_rural.csv  (Figure 4.4 style Euroscepticism % by urban/rural)
  - eu_attachment__breakdown_urban_rural_detail.csv (full Sceptical/Neutral/Pro % by urban/rural, 3 vars)

Run standalone: python parse_eu_attachment.py
"""
import os
import openpyxl
import pandas as pd

BASE_DIR = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish"
XLSX_PATH = os.path.join(BASE_DIR, "ESS11_graphs_Ausra (version2)_20241209.xlsx")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")
SHEET_NAME = "Europ Unif and Attach to Europ"

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
    # numeric year like 2002.0 -> "2002"
    return str(int(v))


# ---------------------------------------------------------------------------
# PART A: Distribution tables (ESS9 2018 vs ESS11 2023), 3 variables:
#   Trust in EU Parliament (eup_cat), Attitude to EU Unification (eunif_cat),
#   Emotional Attachment to Europe (emat_cat)
# ---------------------------------------------------------------------------
def parse_distribution(ws):
    var_blocks = [
        ("Trust in EU Parliament", 7, [7, 8, 9], 11),
        ("Attitude to EU Unification", 13, [15, 16, 17], 19),
        ("Emotional Attachment to Europe", 22, [24, 25, 26], 28),
    ]
    # left block: cols A(label) B(freq) C(percent) D(cum) -> ESS9, 2018
    # right block: cols L(label) M(freq) N(percent) O(cum) -> ESS11, 2023
    blocks = [
        (9, "2018", 1, 2, 3, 4),
        (11, "2023", 12, 13, 14, 15),
    ]
    rows = []
    for var_name, _hdr_row, data_rows, _total_row in var_blocks:
        for ess_round, year, lab_c, freq_c, pct_c, cum_c in blocks:
            for r in data_rows:
                label = cell(ws, r, lab_c)
                if label is None or str(label).strip() == "":
                    continue
                rows.append({
                    "ess_round": ess_round,
                    "year": year,
                    "series": var_name,
                    "response_category": str(label).strip(),
                    "freq": clean_num(cell(ws, r, freq_c)),
                    "percent": clean_num(cell(ws, r, pct_c)),
                    "cum_percent": clean_num(cell(ws, r, cum_c)),
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# PART B: Trend table (rows 29-32): ESS round 1-11, 2 series
# ---------------------------------------------------------------------------
def parse_trend(ws):
    round_row = 29
    year_row = 30
    trust_row = 31
    unif_row = 32
    rows = []
    for c in range(19, 30):  # cols S(19) .. AC(29)
        ess_round = cell(ws, round_row, c)
        year = cell(ws, year_row, c)
        if ess_round is None:
            continue
        ess_round = int(ess_round)
        year_s = year_to_str(year)
        trust_val = clean_num(cell(ws, trust_row, c))
        if trust_val is not None:
            rows.append({
                "ess_round": ess_round, "year": year_s,
                "series": "Trust in EU Parliament", "value": trust_val,
            })
        unif_val = clean_num(cell(ws, unif_row, c))
        if unif_val is not None:
            rows.append({
                "ess_round": ess_round, "year": year_s,
                "series": "Attitude to EU Unification", "value": unif_val,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# PART C: Breakdown by education - Euroscepticism summary (Figure 4.3)
# ---------------------------------------------------------------------------
def parse_breakdown_education_summary(ws):
    header_row = 184
    cats = {
        29: "Low trust in EU Parliament",
        30: "Unification has gone far enough",
        31: "Low attachment to Europe",
    }  # cols AC(29), AD(30), AE(31)
    edu_rows = [185, 186, 187, 188, 189]
    label_col = 28  # AB
    rows = []
    for r in edu_rows:
        group_value = cell(ws, r, label_col)
        if group_value is None:
            continue
        group_value = str(group_value).strip()
        for col, cat_name in cats.items():
            val = clean_num(cell(ws, r, col))
            if val is None:
                continue
            rows.append({
                "category": cat_name,
                "group_type": "education",
                "group_value": group_value,
                "value": val,
                "unit": "percent",
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# PART D: Breakdown by education - detailed Sceptical/Neutral/Pro % per variable
# ---------------------------------------------------------------------------
def parse_breakdown_education_detail(ws):
    # each block: label_row -> header_row = label_row+1, data rows = label_row+3..+5, total = label_row+7
    blocks = [185, 194, 203, 212, 221]
    label_col = 12  # L, used to read the education-level name for the '<Lower Secondary' block only
    var_specs = [
        ("Trust in EU Parliament", 12, 13, 14, 15),        # L,M,N,O
        ("Attitude to EU Unification", 17, 18, 19, 20),    # Q,R,S,T
        ("Emotional Attachment to Europe", 22, 23, 24, 25),  # V,W,X,Y
    ]
    rows = []
    for label_row in blocks:
        group_value = cell(ws, label_row, label_col)
        group_value = str(group_value).strip() if group_value else None
        data_rows = [label_row + 3, label_row + 4, label_row + 5]
        for var_name, lab_c, freq_c, pct_c, cum_c in var_specs:
            for r in data_rows:
                cat_label = cell(ws, r, lab_c)
                if cat_label is None or str(cat_label).strip() == "":
                    continue
                pct = clean_num(cell(ws, r, pct_c))
                if pct is None:
                    continue
                rows.append({
                    "category": f"{var_name} - {str(cat_label).strip()}",
                    "group_type": "education",
                    "group_value": group_value,
                    "value": pct,
                    "unit": "percent",
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# PART E: Breakdown by urban/rural - Euroscepticism summary (Figure 4.4)
# ---------------------------------------------------------------------------
def parse_breakdown_urban_rural_summary(ws):
    cats = {
        28: "Low trust in EU Parliament",       # AB
        29: "Unification has gone far enough",  # AC
        30: "Low attachment to Europe",         # AD
    }
    data = [
        (233, "Urban"),
        (234, "Rural"),
    ]
    rows = []
    for r, group_value in data:
        for col, cat_name in cats.items():
            val = clean_num(cell(ws, r, col))
            if val is None:
                continue
            rows.append({
                "category": cat_name,
                "group_type": "urban_rural",
                "group_value": group_value,
                "value": val,
                "unit": "percent",
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# PART F: Breakdown by urban/rural - detailed Sceptical/Neutral/Pro % per variable
# ---------------------------------------------------------------------------
def parse_breakdown_urban_rural_detail(ws):
    blocks = [
        (233, "Urban", [235, 236, 237]),
        (242, "Rural", [244, 245, 246]),
    ]
    var_specs = [
        ("Trust in EU Parliament", 12, 13, 14, 15),
        ("Attitude to EU Unification", 17, 18, 19, 20),
        ("Emotional Attachment to Europe", 22, 23, 24, 25),
    ]
    rows = []
    for _header_row, group_value, data_rows in blocks:
        for var_name, lab_c, freq_c, pct_c, cum_c in var_specs:
            for r in data_rows:
                cat_label = cell(ws, r, lab_c)
                if cat_label is None or str(cat_label).strip() == "":
                    continue
                pct = clean_num(cell(ws, r, pct_c))
                if pct is None:
                    continue
                rows.append({
                    "category": f"{var_name} - {str(cat_label).strip()}",
                    "group_type": "urban_rural",
                    "group_value": group_value,
                    "value": pct,
                    "unit": "percent",
                })
    return pd.DataFrame(rows)


def main():
    ws = load_ws()

    outputs = {
        "eu_attachment__distribution.csv": parse_distribution(ws),
        "eu_attachment__trend.csv": parse_trend(ws),
        "eu_attachment__breakdown_education.csv": parse_breakdown_education_summary(ws),
        "eu_attachment__breakdown_education_detail.csv": parse_breakdown_education_detail(ws),
        "eu_attachment__breakdown_urban_rural.csv": parse_breakdown_urban_rural_summary(ws),
        "eu_attachment__breakdown_urban_rural_detail.csv": parse_breakdown_urban_rural_detail(ws),
    }

    print(f"=== {SHEET_NAME} ===")
    for fname, df in outputs.items():
        out_path = os.path.join(OUT_DIR, fname)
        df.to_csv(out_path, index=False)
        print(f"\n--> {fname}: {len(df)} rows")
        print(df.head(6).to_string(index=False))
        # sanity checks
        if "value" in df.columns:
            vmin, vmax = df["value"].min(), df["value"].max()
            print(f"    value range: [{vmin}, {vmax}]")
        if "percent" in df.columns:
            vmin, vmax = df["percent"].min(), df["percent"].max()
            print(f"    percent range: [{vmin}, {vmax}]")

    print("\nDone. Files written to:", OUT_DIR)


if __name__ == "__main__":
    main()
