"""
ETL parser for the 'Gender' sheet of
ESS11_graphs_Ausra (version2)_20241209.xlsx  (ESS11 special gender module, Ireland).

This sheet has no ESS-round trend (ESS11-only module) and no overall single-round
distribution table in the requested sense -- every logical table is inherently a
% breakdown by respondent gender (male/female), so only breakdown CSVs are produced.

Each table appears twice in the source: a coarse "summary" row-pair (Male/Female side
by side, seemingly rounded to fewer decimals) AND a detailed per-gender Freq/Percent/Cum
block (found via "-> gndr = Mal" / "-> gndr = Fem" anchors). Spot-checking against the
Irish Social Attitudes 2023 report text confirmed the DETAILED blocks match the report
more precisely (e.g. parental leave: report says top-2-box support Women 73% / Men 63%;
the detailed block gives 72.68% / 63.39% while the coarse summary row gives 64%/73% when
naively summed -- so the detailed blocks were used throughout for consistency/accuracy).

Produces tidy CSVs in data/processed/ (breakdown schema: category, group_type='gender',
group_value=Male/Female, value=percent, unit='percent'):
  - gender__breakdown_unfair_hiring.csv                (Figure 10.1)
  - gender__breakdown_unfair_police.csv                (Figure 10.2)
  - gender__breakdown_medical_equality.csv             (Figure 10.3)
  - gender__breakdown_fair_hiring_perception.csv       (extra table in the sheet, not
        explicitly named in the report text summary -- perception of fairness in hiring/
        pay/promotion generally, as opposed to Fig 10.1's personal-experience question)
  - gender__breakdown_paid_work_attitude.csv           (Figure 10.4, 0-6 scale)
  - gender__breakdown_political_leadership_attitude.csv (Figure 10.5, 0-6 scale)
  - gender__breakdown_business_leadership_attitude.csv (Figure 10.6, 0-6 scale)
  - gender__breakdown_equal_pay_attitude.csv           (Figure 10.7, 0-6 scale)
  - gender__breakdown_parental_leave_attitude.csv      (Figure 10.8, 5-point Likert)

Run standalone: python parse_gender.py
"""
import os
import openpyxl
import pandas as pd

BASE_DIR = r"C:\Users\Gokul\OneDrive\Internship\ESS\Project Florish"
XLSX_PATH = os.path.join(BASE_DIR, "ESS11_graphs_Ausra (version2)_20241209.xlsx")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")
SHEET_NAME = "Gender"

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


# Each table: (filename, label_col, pct_col, categories, male_rows, female_rows)
# Columns are 1-indexed (A=1, B=2, C=3, D=4, E=5 ...)
TABLES = [
    dict(
        fname="gender__breakdown_unfair_hiring.csv",
        pct_col=4,  # D
        categories=["Yes, once", "Yes, more than once", "No",
                    "Have never had job or applied for a job"],
        male_rows=[12, 13, 14, 15],
        female_rows=[24, 25, 26, 27],
    ),
    dict(
        fname="gender__breakdown_unfair_police.csv",
        pct_col=3,  # C
        categories=["Yes, once", "Yes, more than once", "No",
                    "Have never had any contact with the police"],
        male_rows=[38, 39, 40, 41],
        female_rows=[51, 52, 53, 54],
    ),
    dict(
        fname="gender__breakdown_medical_equality.csv",
        pct_col=3,  # C
        categories=["Women are treated less fairly than men",
                    "Men are treated less fairly than women",
                    "Women and men are treated equally fairly"],
        male_rows=[64, 65, 66],
        female_rows=[76, 77, 78],
    ),
    dict(
        fname="gender__breakdown_fair_hiring_perception.csv",
        pct_col=3,  # C
        categories=["Women are treated less fairly than men",
                    "Men are treated less fairly than women",
                    "Women and men are treated equally fairly"],
        male_rows=[90, 91, 92],
        female_rows=[103, 104, 105],
    ),
    dict(
        fname="gender__breakdown_paid_work_attitude.csv",
        pct_col=3,  # C
        categories=["0 - Very bad for family life", "1", "2", "3", "4", "5",
                    "6 - Very good for family life"],
        male_rows=[116, 117, 118, 119, 120, 121, 122],
        female_rows=[132, 133, 134, 135, 136, 137, 138],
    ),
    dict(
        fname="gender__breakdown_political_leadership_attitude.csv",
        pct_col=3,  # C
        categories=["0 - Very bad for politics", "1", "2", "3", "4", "5",
                    "6 - Very good for politics"],
        male_rows=[149, 150, 151, 152, 153, 154, 155],
        female_rows=[166, 167, 168, 169, 170, 171, 172],
    ),
    dict(
        fname="gender__breakdown_business_leadership_attitude.csv",
        pct_col=3,  # C
        categories=["0 - Very bad for businesses", "1", "2", "3", "4", "5",
                    "6 - Very good for businesses"],
        male_rows=[183, 184, 185, 186, 187, 188, 189],
        female_rows=[200, 201, 202, 203, 204, 205, 206],
    ),
    dict(
        fname="gender__breakdown_equal_pay_attitude.csv",
        pct_col=3,  # C
        categories=["0 - Very bad for the economy", "1", "2", "3", "4", "5",
                    "6 - Very good for the economy"],
        male_rows=[218, 219, 220, 221, 222, 223, 224],
        female_rows=[235, 236, 237, 238, 239, 240, 241],
    ),
    dict(
        fname="gender__breakdown_parental_leave_attitude.csv",
        pct_col=3,  # C
        categories=["Strongly in favour", "Somewhat in favour",
                    "Neither in favour nor against", "Somewhat against",
                    "Strongly against"],
        male_rows=[252, 253, 254, 255, 256],
        female_rows=[267, 268, 269, 270, 271],
    ),
]


def parse_table(ws, spec):
    rows = []
    for gender, data_rows in [("Male", spec["male_rows"]), ("Female", spec["female_rows"])]:
        for cat, r in zip(spec["categories"], data_rows):
            val = clean_num(cell(ws, r, spec["pct_col"]))
            if val is None:
                continue
            rows.append({
                "category": cat,
                "group_type": "gender",
                "group_value": gender,
                "value": val,
                "unit": "percent",
            })
    return pd.DataFrame(rows)


def main():
    ws = load_ws()

    print(f"=== {SHEET_NAME} ===")
    total_rows = 0
    for spec in TABLES:
        df = parse_table(ws, spec)
        out_path = os.path.join(OUT_DIR, spec["fname"])
        df.to_csv(out_path, index=False)
        total_rows += len(df)
        print(f"\n--> {spec['fname']}: {len(df)} rows")
        print(df.to_string(index=False))
        print(f"    value range: [{df['value'].min()}, {df['value'].max()}]")

    print(f"\nDone. {len(TABLES)} files written to: {OUT_DIR} ({total_rows} total rows)")


if __name__ == "__main__":
    main()
