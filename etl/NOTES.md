## Trust in Others

**Source sheet:** `Trust in Others` (31 rows x 16 cols).

**Tables found:**
1. Trend table, rows 5-15, cols A (ESS round) / B (Year) / C (Average Trust in Other People). ESS rounds 1-11, 2002-2023.
2. ESS11 (2023) education breakdown, rows 20-24. Row 21 = education-level column headers (`<Lower Secondary`, `Lower Secondary`, `Upper Secondary`, `Advanced Vocational`, `Tertiary`); rows 22-24 = three trust bands (Lower Trust 0-4 / Neutral 5 / Higher Trust 6-10) as percentages. Matches report Figure 1.2 (tertiary = 66% scoring 6-10) exactly.

**CSVs produced:**
- `trust_others__trend.csv` — columns `ess_round, year, series, value`. `series` is always `"Trust in Others"` (single line). 11 rows.
- `trust_others__breakdown_education.csv` — columns `category, group_type, group_value, value, unit`. `group_type="education"`, `unit="percent"`. 15 rows (3 categories x 5 education levels).

**Judgment calls:**
- Fixed the source typo `"Nautral answer (5)"` -> `"Neutral answer (5)"` in the `category` field for readability.
- No ambiguity on units — the breakdown values are plainly percentages (sum to 100 across the 3 trust bands per education level).

## Trust in Institutions

**Source sheet:** `Trust in Institutions` (77 rows x 25 cols). The separate `Sheet1` tab was intentionally skipped (redundant older cut of the education breakdown, per instructions).

**Tables found:**
1. Five Freq/Percent/Cum distribution tables, one per institution: Garda (rows 4-11), Legal System (13-20), Parliament (22-29), Political Parties (31-38), Politicians (40-47). Each has an ESS9 cut (cols A-D, effectively year 2018) side-by-side with an ESS11 cut (cols Q-T, effectively year 2023), response categories Low / Neutral(5) / High.
2. A compact "Low vs High only" summary table interleaved in the same row range (cols F-H for ESS9, cols V-X for ESS11) restating the Low/High percentages for all 5 institutions in one place — this is the direct source of report Figure 2.1, but it is **fully redundant** with the 5 per-institution distribution tables (same numbers, just missing the Neutral row and Freq/Cum), so it was **not** re-emitted as its own CSV.
3. Trend table, rows 50-61 (cols Q-W): mean trust score (0-10 scale) 2002-2023 for Garda / Legal System / Parliament / Politicians / Political Parties. Political Parties has no value for round 1 (2002) — the question wasn't asked that round, so that row is simply absent from the tidy output rather than filled with a placeholder.
4. Education breakdown, rows 71-77 (ESS11, 2023): % with high trust (6-10) by education level, for Police/Legal System/Parliament/Political Parties/Politicians. Matches report Figure 2.3.

**CSVs produced:**
- `trust_institutions__trend.csv` — 54 rows (11 rounds x 5 institutions, minus the 1 missing Political Parties/round-1 value).
- `trust_institutions__breakdown_education.csv` — 25 rows (5 education levels x 5 institutions), `unit="percent"`.
- `trust_institutions__distribution_garda.csv`, `..._legal_system.csv`, `..._parliament.csv`, `..._political_parties.csv`, `..._politicians.csv` — one file per institution, 6 rows each (2 rounds x 3 response categories: Low/Neutral/High).

**Judgment calls / ambiguities:**
- The sheet labels the same institution "Garda" in some places and "Police" in others (e.g. row 4 says "Garda", row 72 header says "Police", distribution sub-labels say "Police"). Standardized on **"Garda"** across all output CSVs for consistency with the sheet's own top-level block label and with the report's terminology.
- Renamed response categories for clarity/consistency: `"Low"`→`"Low Trust (0-4)"`, `"Nautral answer (5)"`→`"Neutral answer (5)"`, `"High"`→`"High Trust (6-10)"` (ESS9 side); ESS11 side already used `"Lower Trust (0-4)"`/`"Higher Trust (6-11)"` labels, normalized to match (the "6-11" in the source is a labeling typo — the underlying variable is the standard 0-10 scale, so normalized to "6-10").
- ESS round → year mapping for the distribution tables (round 9 = 2018, round 11 = 2023) was not stated as a literal year value inside those specific table blocks (only "ESS9"/"ESS11" labels) — taken from the sheet's own trend table (rows 50-61) which does give literal years for each round number.
- Verified against report: Garda 68.97% high trust (ESS11) matches report's "69%"; Legal System 58.35% matches report's "58%".

## Life Sat and Happiness

**Source sheet:** `Life Sat and Happiness` (119 rows x 26 cols).

**Tables found:**
1. Rows 4-77 (cols A-O): 11 repeating `essround = N` blocks, each with a Stata-style summary-statistics table (Variable/Obs/Weight/Mean/Std.dev/Min/Max) for `stflife` and `happy`. This duplicates the same round-by-round means found in the cleaner trend table (item 2 below) — **not** re-emitted separately, since it would just be the identical numbers under a clunkier schema.
2. Rows 4-16 (cols Q-T): ready-made tidy trend table — ESS round (`R1`..`R11`), Year, Life Satisfaction mean, Happiness mean, 2002-2023. Used as the trend CSV source. 2023 values: Life Satisfaction 7.38 (report rounds to "7.4"), Happiness 7.71 (report ~"7.7") — matches.
3. Rows 80-119: ESS11 (2023) "Life Satisfaction and Employment Status" table (report Table 5.1). Rows 84-88 (cols F-H) give a compact summary — 5 employment-status groups (In paid work / Unemployed looking for job / Inactive not looking for a job / Refusal-Don't know / Total Population) with Percent Satisfied / Percent Dissatisfied directly. There are also more granular per-group Freq/Percent/Cum sub-tables further down (rows 89-119) containing the identical percentages with frequency counts — redundant with the compact summary table, not re-emitted.

**CSVs produced:**
- `life_satisfaction_happiness__trend.csv` — 22 rows (11 rounds x 2 series: Life Satisfaction, Happiness).
- `life_satisfaction_happiness__breakdown_employment.csv` — 10 rows (5 employment groups x 2 categories: Satisfied/Dissatisfied), `unit="percent"`.

**Judgment calls:**
- Verified against report Table 5.1: In paid work 86.21/13.79 (report 86.2/13.8), Unemployed 70.84/29.16 (report 70.8/29.2), Inactive 85.01/14.99 (report 85.0/15.0), Refusal/DK 16.54/83.46 (report 16.5/83.5), Total 85.05/14.95 (report 85.1/15.0) — small rounding differences only, confirms correct table read.

## Econ Sat and HH Inc Adequacy

**Source sheet:** `Econ Sat and HH Inc Adequacy` (212 rows x 15 cols). The separate `Economic Sat` tab was intentionally skipped (older superseded draft dated 2020, only covers up to round 9, per instructions).

**Tables found:**
1. Rows 3-14 (cols F-H): ready-made tidy trend table — ESS round, Year, % Satisfied with the present state of the economy, 2002-2023. Report Figure 6.1.
2. Rows 3-82 (cols A-D): 11 repeating per-round `satecon` Freq/Percent/Cum distribution blocks (round number as a bare float in col A headers each block), Satisfied/Dissatisfied rows + Total.
3. Rows 86-136: ESS11 (2023) satisfaction with the economy by age group (report Figure 6.2). Used the 7 per-age-group Freq/Percent/Cum sub-tables (each with a Satisfied and a Dissatisfied row) rather than the single-row "Satisfied only" summary matrix at row 89, since the sub-tables give both percentages and are more complete.
4. Rows 138-212: ESS11 (2023) perception of household income adequacy by income quintile (report Figure 6.3). Used the compact ready-made matrix at rows 140-144 (quintile columns Bottom 20% / 2nd / 3rd / 4th / Top 20% / All; category rows "Living comfortably" / "Coping" / "Finding it difficult" / "Finding it very difficult"). The more verbose per-quintile Freq/Percent/Cum sub-tables further down (rows 144-212, using slightly different category labels like "Living comfortably on present income") contain the same percentages and were treated as redundant, not re-emitted.

**CSVs produced:**
- `economic_satisfaction__trend.csv` — 11 rows, `series="Economic Satisfaction"`.
- `economic_satisfaction__distribution.csv` — 22 rows (11 rounds x Satisfied/Dissatisfied).
- `economic_satisfaction__breakdown_age.csv` — 14 rows (7 age groups x Satisfied/Dissatisfied), `unit="percent"`.
- `economic_satisfaction__breakdown_income_quintile.csv` — 23 rows (4 categories x 6 quintile groups, minus 1 legitimately-missing cell: "Finding it very difficult" x "Top 20%" was blank in the source, presumably suppressed for small sample size — left out rather than filled with 0). `unit="percent"`.

**Judgment calls:**
- Labeled the 2nd/3rd/4th quintile columns (source header just says bare numbers `2`, `3`, `4`) as `"2nd quintile"`, `"3rd quintile"`, `"4th quintile"` for readability; `"Bottom 20%"`, `"Top 20%"`, and `"All"` were already labeled that way in the source.
- Round -> year mapping for the per-round distribution blocks was taken from the sheet's own trend table (rows 3-14), since the distribution blocks themselves only label rounds with bare numbers, not years.

## Climate Change

**Source sheet:** `Climate Change` (8 rows x 23 cols) — small, single wide table.

**Tables found:**
1. Rows 4-8: ESS round numbers (9, 10, 11) and years (2016, "2021/22", 2023) as column headers in row 4/5, three climate-perception questions as rows 6-8 with mean scores (0-10 scale) per round.

**CSVs produced:**
- `climate_change__trend.csv` — 9 rows (3 questions x 3 rounds). Shortened the verbatim (very long) question text into stable `series` labels: `"Limiting energy use would reduce climate change"`, `"People will actually limit energy use"`, `"Governments will take sufficient action"`.

**Judgment calls:**
- Verified against report Figure 9.1: 2023 means — reduce-climate-change likelihood 6.1059 (report "6.11"), people-will-limit-energy 4.4839 (report "4.5"), governments-will-act 4.9999 (report "5.0"); 2016 people-will-limit-energy 4.3 exactly matches report's "4.3". Confirms correct table read; `unit` is implicitly `mean_0_10` (not included as a column per the trend CSV schema, but noted here since all three series are means on an 11-point 0-10 scale, not percentages).

## Europ Unif and Attach to Europ

**Source sheet:** `Europ Unif and Attach to Europ` (248 rows x 37 cols).

**Tables found:**
1. Rows 4-28: two side-by-side Freq/Percent/Cum distribution tables (ESS9/2018 in cols A-D, ESS11/2023 in cols L-O) for three variables: Trust in EU Parliament (`eup_cat`), Attitude to EU Unification (`eunif_cat`), Emotional Attachment to Europe (`emat_cat`), each with 3 response categories (Sceptical European / Neutral answer (5) / Pro-European). A small companion "figure" table (cols F-H / Q-S) restates just the Pro-European/Sceptical-European percentages for all 3 variables -- fully redundant with the distribution tables, not separately emitted.
2. Rows 29-181: a ready-made compact trend table (rows 29-32, cols R-AC: ESS round, Year, mean `trstep` and mean `euftf` 2002-2023) plus 11 repeating `essround = N` Stata-style summary-stat blocks per variable (rows 35-179) that duplicate the same means -- the compact table was used as the trend source, the stat blocks were not re-parsed. No historical trend exists in the source for Emotional Attachment (`emat`) -- it appears to be an ESS11-only question, so only 2 series (not 3) appear in the trend CSV.
3. Rows 184-228 (ESS11, 2023): breakdown by education, containing (a) a "Euroscepticism" summary table (cols AB-AE: % Low trust in EU Parliament / % Unification has gone far enough / % Low attachment to Europe, by 5 education levels -- matches report Figure 4.3 exactly) and (b) the full Sceptical/Neutral/Pro-European % breakdown per variable per education level (cols L-Y).
4. Rows 232-248 (ESS11, 2023): same structure as #3 but for Urban vs Rural residence (matches report Figure 4.4).

**CSVs produced:**
- `eu_attachment__distribution.csv` -- columns `ess_round, year, series, response_category, freq, percent, cum_percent` (added a `series` column beyond the base spec since this sheet has 3 distinct distribution variables sharing the same round/year, unlike Relig's single variable). 18 rows (2 rounds x 3 variables x 3 categories).
- `eu_attachment__trend.csv` -- 20 rows (11 rounds x Trust in EU Parliament, 9 rounds x Attitude to EU Unification -- rounds 1 and 5 are legitimately missing for the unification question, 0 obs in source).
- `eu_attachment__breakdown_education.csv` -- the Figure-4.3-style Euroscepticism summary, 15 rows (5 education levels x 3 "Low X" categories), `unit="percent"`.
- `eu_attachment__breakdown_education_detail.csv` -- the fuller Sceptical/Neutral/Pro-European breakdown, 45 rows (5 education levels x 3 variables x 3 categories). `category` is prefixed with the variable name (e.g. `"Trust in EU Parliament - Sceptical European"`) since the breakdown schema has no separate metric column.
- `eu_attachment__breakdown_urban_rural.csv` -- Figure-4.4-style summary, 6 rows.
- `eu_attachment__breakdown_urban_rural_detail.csv` -- fuller breakdown, 18 rows.

**Judgment calls / ambiguities:**
- Added a `series` column to the distribution CSV (not in the base spec) since 3 distinct variables share identical ESS-round/year distribution structure in this sheet; kept all other required columns intact.
- Split education and urban/rural breakdowns each into a "summary" (Euroscepticism framing, matches report figures directly) and "detail" (full 3-category breakdown) file rather than merging, since they are visually and structurally distinct tables in the source, and merging would require inventing a metric column not in the spec.
- Fixed source typos in category labels: "Low attachment ot Europe" -> "Low attachment to Europe".
- Sanity check: all percentages fall in [13, 70]; all trend means fall in [4.1, 5.9], consistent with an 0-10 trust/attitude scale and the report's Figure 4.2 narrative (low point ~2010, values 4-5).

## Immigration

**Source sheet:** `Immigration` (189 rows x 25 cols).

**Tables found:**
1. Rows 3-97: a ready-made compact trend table (rows 3-7, cols I-T: ESS round, Year, mean score 0-10 for Economy/Culture/Place to live, 2002-2023) plus 11 repeating `essround = N` Stata-style summary-stat blocks (rows 4-97, variables `imbgeco`/`imueclt`/`imwbcnt`) that duplicate the same means exactly -- the compact table was used as the trend source; the stat blocks were not re-parsed.
2. Rows 100-140 (ESS11, 2023): breakdown by education -- a summary table (cols P-S: % positive view of Economy/Culture/Place to live by 5 education levels, matches report Figure 7.2 exactly, e.g. Tertiary 78.24/80.62/79.62 vs report's "tertiary ~80%") plus, per education level, three parallel Negative-view/Positive-view Freq/Percent/Cum sub-tables (one per metric, cols A-D / F-I / K-N).
3. Rows 142-189 (ESS11, 2023): breakdown by employment status (In paid work / Unemployed) -- a summary table (row 143-145, cols F-I, matches report Figure 7.3, e.g. Economy gap 65.93-52.46=13.5pp vs report's "14pp") plus, per metric, separate Negative/Positive Freq/Percent/Cum sub-tables for each employment status.

**CSVs produced:**
- `immigration__trend.csv` -- 33 rows (11 rounds x 3 series: Economy, Culture, Place to live).
- `immigration__breakdown_education.csv` -- Figure-7.2-style % positive view summary, 15 rows (5 education levels x 3 metrics), `unit="percent"`.
- `immigration__breakdown_education_detail.csv` -- Negative/Positive view % breakdown, 30 rows (5 education levels x 3 metrics x 2 categories). `category` prefixed with metric name (e.g. `"Economy - Negative view"`).
- `immigration__breakdown_employment.csv` -- Figure-7.3-style summary, 6 rows.
- `immigration__breakdown_employment_detail.csv` -- Negative/Positive breakdown, 12 rows.

**Judgment calls / ambiguities:**
- No overall single-round distribution CSV was produced for this sheet -- unlike Relig/eu_attachment, there is no standalone "all of Ireland, one round, Freq/Percent/Cum" table in the source; every Freq/Percent/Cum block here is already scoped to an education or employment sub-group, so it belongs in the breakdown files.
- Sanity check against report: trend Economy 2010 low point 4.4756 (report "4.5"), 2021/22 6.6019 (report "6.6"); Culture 2002 5.59 -> 2023 6.28 (report "5.6->6.7" 2021/22=6.72, matches); Place-to-live 2002 5.36 -> 2021/22 6.87 (report "5.4->6.9"), 2023 dips to 6.26 (report notes a dip by 2023) -- all consistent. Education breakdown: lowest-education group (`<Lower Secondary`) Place-to-live positive 36.71% vs report's "~37%"; Tertiary 79.62% vs report's "~80%" -- matches "widest gap" narrative.

## Relig

**Source sheet:** `Relig` (185 rows x 21 cols). The separate `Religion` tab was intentionally **not** read (older superseded draft dated 2020, only goes to ESS round 9, per instructions).

**Tables found:**
1. Rows 4-6: ready-made compact trend table (ESS round, Year, % belonging to a religion "Yes", 2002-2023). Matches report Figure 8.1 (2004: 86.25% vs report's "86%"; 2023: 68.09% vs report's "68%").
2. Rows 10-158: 11 repeating `-> essround = N` blocks, each with a Freq/Percent/Cum distribution table for Yes/No belonging. Column position of the Freq/Percent/Cum block shifts by one column for rounds 10 and 11 (cols B-D instead of C-E) -- handled generically by scanning each block for the `"Freq."` header cell rather than hardcoding a single column offset.
3. Rows 29-49 (cols H-U): a secondary "Born in country" x "Belonging" cross-tab count/percentage trend table. **Out of scope** for the requested breakdowns (gender/age/education/location) and not extracted -- noted here for completeness in case it's wanted later.
4. Rows 162-185 (ESS11, 2023): Table 8.2 -- % Yes/No belonging to a religion, broken down by 4 dimensions in sequence: Gender (rows 167-168), Age (170-176), Highest Completed Education (178-182), Location/Urban-Rural (184-185).

**CSVs produced:**
- `religion__trend.csv` -- 11 rows.
- `religion__distribution.csv` -- 22 rows (11 rounds x Yes/No).
- `religion__breakdown_gender.csv` -- 4 rows (2 genders x Yes/No), `unit="percent"`.
- `religion__breakdown_age.csv` -- 14 rows (7 age groups x Yes/No).
- `religion__breakdown_education.csv` -- 10 rows (5 education levels x Yes/No).
- `religion__breakdown_urban_rural.csv` -- 4 rows (Urban/Rural x Yes/No).

**Judgment calls / ambiguities:**
- The "Born in country" cross-tab (item 3 above) was deliberately excluded -- it's a legitimate table in the sheet but doesn't map to any of the four requested breakdown dimensions (gender/age/education/location), and the task explicitly scoped Relig to "Table 8.2" style breakdowns only.
- Verified against report Table 8.2 almost exactly: Male 64.37/35.63 (report 64.4/35.6), Female 71.67/28.33 (report 71.7/28.3), age "25 and under" 55.78/44.22 (report 55.8/44.2), "76 plus" 86.23/13.77 (report 86.2/13.8), Urban 64.20/35.80 (report matches), Rural 72.06/27.94 (report "72.1/27.9") -- tiny rounding differences only, confirms correct table read.

## Gender

**Source sheet:** `Gender` (273 rows x 16 cols) -- ESS11 special gender module, Ireland. No ESS-round trend exists in this sheet (ESS11-only module), so no trend CSV was produced.

**Tables found (9 distinct logical tables, each split by respondent gender):**
1. Unfairly treated in hiring/pay/promotion because of gender (rows 2-29) -- report Figure 10.1.
2. Unfairly treated by the police because of gender (rows 31-56) -- report Figure 10.2.
3. Perceived fairness of gender treatment seeking medical treatment (rows 57-80) -- report Figure 10.3.
4. Perceived fairness of gender treatment in hiring/pay/promotion generally (rows 81-107) -- **an extra table not explicitly named in the report text excerpt provided**; distinct from table 1 (which asks about the respondent's own personal experience) -- this one asks about perceived societal fairness, structurally identical to table 3's response categories (Women treated less fairly / Men treated less fairly / Equally fairly).
5. Whether equal numbers of women/men in paid work is bad/good for family life, 0-6 scale (rows 109-140) -- report Figure 10.4.
6. Whether equal numbers of women/men in political leadership is bad/good for politics, 0-6 scale (rows 142-174) -- report Figure 10.5.
7. Whether equal numbers of women/men in business leadership is bad/good for business, 0-6 scale (rows 176-208) -- report Figure 10.6.
8. Whether equal pay for equal work is bad/good for the economy, 0-6 scale (rows 210-243) -- report Figure 10.7.
9. Support for requiring both parents to take equal parental leave, 5-point Likert (rows 245-273) -- report Figure 10.8.

Each table has two representations in the source: a coarse "summary" row-pair (Male/Female side by side near the top of each section) and a detailed per-gender Freq/Percent/Cum block (found via `-> gndr = Mal` / `-> gndr = Fem` anchors). **The detailed blocks were used throughout**, after spot-checking showed they match the report more precisely than the coarse summary rows -- e.g. for parental leave, the coarse summary row sums to Male 64%/Female 74% (top-2-box), while the detailed block gives 63.39%/72.68%, which matches the report's stated "Women 73%, Men 63%" exactly.

**CSVs produced (breakdown schema: `category, group_type="gender", group_value=Male/Female, value, unit="percent"`):**
- `gender__breakdown_unfair_hiring.csv` -- 8 rows.
- `gender__breakdown_unfair_police.csv` -- 8 rows.
- `gender__breakdown_medical_equality.csv` -- 6 rows.
- `gender__breakdown_fair_hiring_perception.csv` -- 6 rows (the extra table, #4 above).
- `gender__breakdown_paid_work_attitude.csv` -- 14 rows (0-6 scale, 7 points x 2 genders).
- `gender__breakdown_political_leadership_attitude.csv` -- 14 rows.
- `gender__breakdown_business_leadership_attitude.csv` -- 14 rows.
- `gender__breakdown_equal_pay_attitude.csv` -- 14 rows.
- `gender__breakdown_parental_leave_attitude.csv` -- 10 rows (5-point Likert x 2 genders).

**Judgment calls / ambiguities:**
- Category labels for the four 0-6 scale tables (5-8) were built as `"0 - Very bad for X"` ... `"6 - Very good for X"` since the source only labels the two endpoints textually and the 5 interior points as bare numbers 1-5; kept the numeric points as plain `"1"`.."5"` strings and only annotated the endpoints, to stay faithful to the source rather than inventing labels for the middle categories.
- `unit="percent"` for all rows including the 0-6/5-point scale tables -- these are % of respondents choosing each scale point (a response distribution), not a mean score, so "percent" is correct (not `mean_0_6`).
- Values cross-checked extensively against the report and matched closely everywhere a same-named figure existed (Fig 10.1: Male 8.7% vs 8%, Female 17.89% vs 18%; Fig 10.4 aggregated 4+: Male 77.35% vs 77%, Female 76.6% vs 77%; Fig 10.5 aggregated 4-6: Male 77.32% vs 77%, Female 85.04% vs 85%; Fig 10.6: Male 82.54% vs 83%, Female 88.47% vs 88%; Fig 10.7: Male 86.61% vs 87%, Female 93.9% vs 94%; Fig 10.8 top-2: Male 63.39% vs 63%, Female 72.68% vs 73%) -- confirms both the table identification and the choice to use the detailed blocks over the coarse summary rows.

## Health and Health Services

**Source sheet:** `Health and Health Services` (636 rows x 17 cols). Parser: `etl/parse_health.py` — runnable standalone, prints per-file `.head()` and value-range sanity checks.

**Tables found:**
1. Rows 2-5 (cols F-Q): ready-made trend table — ESS round 1-11, year (2002...2023, round 10 kept as the literal string `"2021/2022"`), % "Very good" self-rated health and % "Fair/bad/very bad" self-rated health. Report Figure 3.1.
2. Rows 4-118: 11 repeating `essround = N` blocks, each a `health_cat` Freq/Percent/Cum distribution (Very good / Good / Fair-bad-very bad + Total). Located generically by scanning the whole sheet for every literal `"Freq."` cell (62 such blocks total in this sheet) rather than hardcoding row numbers, since the label/data columns shift around depending on section (see judgment calls).
3. Rows 121-130 (cols F-H): a compact "Very good"/"Fair/bad/very bad" % summary table combining Employment status (In paid work, Unemployed) and Education level (<Lower Secondary…Tertiary) into one bar-chart source table for report Figure 3.2. **Confirmed fully redundant** with the detailed per-group `health_cat` sub-tables at rows 124-189 (values match exactly) — not re-emitted separately; the richer 3-category (Very good/Good/Fair-bad-very bad) detailed sub-tables were used instead.
4. Rows 190-288: Figure 3.3 "Good Health and the Income Distribution" — a compact decile-summary row (190-191, `Percent in good health` by Bottom/2/…/Top) plus 10 detailed per-decile `good_health` (Otherwise/Good) Freq/Percent/Cum sub-tables labelled numerically `1.0`-`10.0`. The detailed sub-tables were used as the authoritative source (their values reproduce the summary row exactly for deciles 1-5,7-10, decile 6 has a copy-paste glitch in the source — see below).
5. Rows 298-434: Figure 3.4 "Satisfaction with the Health Care System and 'Very Good' Health, by Age" — a compact 2-series summary matrix (rows 298-300, age bands 25-and-under...76-plus) plus detailed per-age-band `sat_health` (Satisfied/Dissatisfied) sub-tables (rows 302-363) and detailed per-age-band `health_cat` (Very good/Good/Fair-bad-very bad) sub-tables (rows 368-434). The detailed sub-tables were used (richer categories, values match the summary matrix exactly).
6. Rows 438-636: Figure 3.5 "Happiness, General Health and the Income Distribution" — a second compact decile-summary table (rows 439-441, Good health % and Happy % by decile) plus a **near-duplicate** set of 10 detailed `good_health` sub-tables (rows 442-532, decile labels Bottom/2/…/Top this time) and a genuinely new set of 10 `happy_b` (Happy/Unhappy) sub-tables (rows 541-631).

**CSVs produced:**
- `health__trend_selfreported_health.csv` — `ess_round, year, series, value`. 22 rows (11 rounds x 2 series: "Very good health", "Fair/bad/very bad health").
- `health__distribution_selfreported_health.csv` — `ess_round, year, response_category, freq, percent, cum_percent`. 33 rows (11 rounds x 3 categories). `Total` rows dropped (not a response category).
- `health__breakdown_employment_education.csv` — `category, group_type, group_value, value, unit`. 21 rows: `group_type="employment"` (2 groups: In paid work, Unemployed looking for job) + `group_type="education"` (5 levels: <Lower Secondary, Lower Secondary, Upper Secondary, Advanced Vocational, Tertiary), each x 3 health categories. `unit="percent"`.
- `health__breakdown_income_decile.csv` — 40 rows: `category` in {Good health, Not good health} (renamed from source's Good/Otherwise) x 10 deciles, plus `category` in {Happy, Unhappy} x 10 deciles. `group_type="income_decile"`, `group_value` in Bottom/2/…/9/Top. `unit="percent"`. Built from the **first** good-health decile block (rows 193-283) and the happy decile block (rows 541-631) — see judgment calls for why the second good-health decile block (rows 442-532) was skipped.
- `health__breakdown_age.csv` — 35 rows: healthcare-satisfaction (2 categories x 7 age bands) + self-rated health (3 categories x 7 age bands), `group_type="age"`, categories suffixed `(healthcare system)` / `(self-rated health)` to disambiguate the two metrics sharing one file. `unit="percent"`.

**Judgment calls / ambiguities:**
- All values in this sheet are plain percentages (0-100), so `unit="percent"` throughout — no mean/0-10-scale tables appear in this sheet (those live in other sheets, e.g. Climate Change, Gender).
- **Income-decile data quality issue**: the source has two separate copies of the "Good health % by income decile" table (rows 193-283 vs rows 442-532). They agree for 8 of 10 deciles but disagree for decile 6 (83.99% in the first copy vs 83.82% in the second) and decile "Top" (87.10% in the first copy vs 85.65% in the second — the second copy also literally differs in which value is labelled "Top" vs "9"). The first copy's decile-6 value (83.99%) is suspiciously identical to decile 5's value, suggesting a copy-paste error at that specific cell; the first copy is also the one whose numbers exactly reproduce the sheet's own Figure-3.3 summary row (rows 190-191), so it was treated as authoritative and used in `health__breakdown_income_decile.csv`; the second copy (rows 442-532) was not re-emitted, to avoid publishing two silently-conflicting numbers for the same metric under the same file. Flagging here in case the true source-of-truth should actually be the second copy.
- The Employment+Education summary chart table (rows 121-130) and the Figure-3.4 age summary matrix (rows 298-300) were both confirmed byte-for-byte redundant with their corresponding detailed Freq/Percent/Cum sub-tables and were not separately emitted, consistent with the "prefer natural table boundaries, avoid redundant files" guidance.
- Generic block-location strategy: rather than hardcoding row numbers (which are extremely fragile given this sheet's inconsistent spacing/column-offsets between sections), the parser scans the whole sheet for every cell literally equal to `"Freq."`, derives `label_col = that_column - 1`, `percent_col = +1`, `cum_col = +2` from its position, and finds each block's group label (e.g. "In paid work", a decile number, an age band) by scanning upward for the nearest non-empty cell in columns 1..label_col. This handled the sheet's frequent column-offset shifts (e.g. the age-satisfaction sub-tables use column C or D for "Freq." depending on how wide the row label text is, instead of a fixed column B) without needing per-block special-casing.

## Hlth inequalities

**Source sheet:** `Hlth inequalities` (359 rows x 17 cols) — the ESS11-only rotating "Social Inequalities in Health" module. There is no ESS-round trend anywhere in this sheet (single round, 2023) and, contrary to the task brief's guess, **no demographic (education/employment/age/gender) breakdowns appear in this sheet at all** — every table here is a single, whole-of-Ireland-sample distribution or an item-level battery. Parser: `etl/parse_health_inequalities.py`.

**Tables found (4 sections, all ESS round 11 / year 2023):**
1. Rows 2-171: "Health problems, last 12 months" — a 12-item checkbox battery (Diabetes, Severe headaches, Heart or circulation problem, Skin condition related, Allergies, Breathing problems, Stomach or digestion related, Muscular/joint pain hand-or-arm, High blood pressure, Muscular/joint pain foot-or-leg, Back or neck pain, None of these). A clean summary bar-chart table (rows 6-17, cols F-G) gives one % per item; 12 detailed Marked/Not-marked Freq/Percent/Cum sub-tables follow (values match the summary exactly). Report Figure 3.5 (second, mislabeled "3.5" in the report, rotating-module figure).
2. Rows 160-171: "Unable to get medical consultation or treatment in the last 12 months" — simple Yes/No Freq/Percent/Cum distribution. Report Figure 3.6.
3. Rows 175-254: "Feelings in the past week" — 8-item CES-D-style battery (Felt depressed / Felt everything did as effort / Sleep was restless / Were happy / Felt lonely / Enjoyed life / Felt sad / Could not get going), each on a 4-point frequency scale (None or almost none / Some / Most / All or almost all of the time). A clean summary matrix (rows 177-184, cols F-J) gives all 8x4 percentages directly; 8 detailed per-item Freq/Percent/Cum sub-tables follow in the *same item order* as the summary matrix. Report Figure 3.7.
4. Rows 256-359: "Problems with accommodation" — an 8-item checkbox battery (Mould or rot in windows/doors/floors, Damp walls or leaking roof, Overcrowding, Presence of insects or rodents, Extremely hot or extremely cold, Noise, Neither bath nor shower, Lack of indoor flushing toilet). Same structure as section 1: clean summary table (rows 258-265, cols F-G) + 8 detailed Marked/Not-marked sub-tables. Report Figure 3.8.

**CSVs produced:**
- `health_inequalities__distribution_health_problems_12m.csv` — `ess_round, year, response_category, freq, percent, cum_percent`. 12 rows, one per condition (the "Marked" / prevalence row only — see judgment calls for why `cum_percent` is blank).
- `health_inequalities__distribution_unable_medical_treatment.csv` — 2 rows (Yes/No), full `cum_percent` populated (it's a genuine 2-category mutually-exclusive distribution).
- `health_inequalities__breakdown_feelings_past_week.csv` — `category, group_type, group_value, value, unit`. 32 rows (8 items x 4 frequency categories), `group_type="feeling_item"`, sourced from the clean summary matrix (rows 177-184). Treated as the primary/authoritative file for this section.
- `health_inequalities__breakdown_feelings_past_week_detailed.csv` — same shape, 32 rows, but sourced from the 8 detailed Freq/Percent/Cum sub-tables instead — kept as a **separate supplementary file** because its values differ slightly from the summary matrix (see judgment calls) rather than silently overwriting/averaging them.
- `health_inequalities__distribution_accommodation_problems.csv` — 8 rows, one per accommodation problem.

**Judgment calls / ambiguities:**
- **Row-label reconstruction workaround**: this sheet's long row labels (e.g. "Health problems, last 12 months: heart or circulation problem") were typed as several stacked single-word/phrase fragments across consecutive physical rows (manual word-wrap, not a real merged cell), so naive concatenation of the fragments is unreliable (e.g. one fragment literally reads "accomodatio" and the next "n: mould or...", split mid-word with no space). Instead, each detailed checkbox sub-table's "Marked" percentage was matched **by value** against the item names in that section's own clean summary chart table (all percentages within a section are unique to 2 decimal places, so this is a safe/robust join). All 12 health-problem items and all 8 accommodation items resolved with no `UNKNOWN` fallbacks (verified explicitly after running the parser).
- **`cum_percent` left blank for the two checkbox-battery distribution CSVs** (health problems, accommodation problems): each item is an independent yes/no checkbox (respondents can mark multiple), not a mutually-exclusive categorical variable, so a cumulative percentage across items has no real meaning. `freq`/`percent` (the "Marked" / prevalence figures) are populated normally.
- **Feelings-battery value discrepancy**: the clean summary matrix (rows 177-184) and the 8 detailed per-item Freq/Percent/Cum sub-tables give slightly different percentages for the same item/frequency-category cell — e.g. "Felt depressed" x "None or almost none of the time" is 77.42% in the summary matrix vs 76.91% in the detailed sub-table (differences up to ~0.5pp throughout, likely a different missing-data/weighting base between the two computations in the original Stata output). Rather than picking one and discarding the other, both were emitted as separate files (`..._feelings_past_week.csv` = summary matrix, `..._feelings_past_week_detailed.csv` = detailed sub-tables with counts) so downstream consumers can choose; the summary-matrix file is recommended as primary since it matches the report figure's likely source table more directly.
- No units ambiguity: every value in this sheet is a plain percentage of the ESS11 Irish sample; `unit="percent"` throughout.

## C19 - Personal experience

**Source sheet:** `C19 - Personal experience` (146 rows x 28 cols).

**ESS round / year for all three C19 sheets:** the sheet carries no `essround =` marker of its own. The COVID-19 module was fielded once in the Irish ESS series, as a rotating module in **ESS Round 10** (Irish fieldwork **2021/22** - delayed by the pandemic, run shortly before the Round 11/2023 fieldwork that the rest of this workbook otherwise covers). This is corroborated by the accompanying PDF report, which attributes its other rotating-module content ("Inequalities in Health") explicitly to "round 10", and separately calls the pre-2023 wave "2021/2". All C19 sheets are tagged `ess_round=10`, `year="2021/22"` on this basis - flagged here as an inference rather than a value read directly off the sheet.

**Tables found** (anchored programmatically by scanning for `Freq./Percent/Cum.` header triplets, titled using the sheet's own "Figure X: ..." captions):
1. "Respondent had COVID-19" - 3-category Freq/Percent/Cum distribution (Total N=1747).
2. "Someone at home had COVID-19" - 4-category Freq/Percent/Cum distribution (Total N=1757).
3. Six independent yes/no checklist items ("things that happened since the start of COVID-19": made redundant/lost job, income reduced, working hours reduced, furloughed, forced unpaid leave, none of these), each its own binary Not-marked/Marked Freq/Percent/Cum table (Total N=1675, except "none of these" N=1770 - a genuine source discrepancy, left as-is).

**CSVs produced:**
- `c19_personal_experience__distribution_had_covid19.csv` - 3 rows.
- `c19_personal_experience__distribution_household_covid19.csv` - 4 rows.
- `c19_personal_experience__distribution_pandemic_impacts.csv` - 12 rows (6 items x Marked/Not marked), `response_category` prefixed with the item name (e.g. `"Furloughed: Marked"`) to keep all six checklist items in one tidy file without adding a non-spec column.

**Judgment calls / ambiguities:**
- ESS round/year is inferred (see above), not read literally from this sheet.
- Two of the six checklist sub-tables ("unpaid leave/holiday" and "none of these") have a data-entry quirk: the true category label ("Not marked"/"Marked") is duplicated across two adjacent columns, with the header's own label column instead holding a stray fragment ("ay", "these") of the wrapped question title. Resolved generically by taking the left-most non-blank cell in each row as the label (verified correct against all 6 tables' output).

## C19 - Prioritisations

**Source sheet:** `C19 - Prioritisations` (250 rows x 23 cols). Same ESS round/year basis as above: `ess_round=10`, `year="2021/22"`.

**Tables found:** three 11-point (0-10) attitude scales, each printed three times over:
1. An OVERALL Freq/Percent/Cum distribution table (11 categories: 2 text endpoints + numeric midpoints 1-9).
2. Three PER-GROUP Freq/Percent/Cum sub-tables (one per "personal C19 experience" group: tested positive / think had it / never had it) - redundant with (3), not re-emitted.
3. One wide cross-tab table restating the same 3-group breakdown as side-by-side percent columns - used as the breakdown CSV source.

The three questions: "more important to prioritise public health or economic activity" (0=public health, 10=economic activity), "more important to monitor/track the public or maintain privacy" (0=monitor/track, 10=privacy), "more important to follow government rules or make own decisions" (0=follow rules, 10=own decisions).

**CSVs produced:**
- `c19_prioritisations__distribution_health_vs_economy.csv`, `..._distribution_privacy_vs_monitoring.csv`, `..._distribution_rules_vs_own_decisions.csv` - 11 rows each.
- `c19_prioritisations__breakdown_c19_experience.csv` - 94 rows (3 questions x 11 categories x 3 groups, minus a handful of source cells that were genuinely blank/suppressed - left out rather than filled with 0). `group_type="c19_experience"`, `category` prefixed with the question slug (e.g. `"health_vs_economy: 3"`), `unit="percent"`.

**Judgment calls / ambiguities:**
- The two text endpoint labels (value 0 and value 10) are truncated to ~40 characters in the OVERALL vertical tables' own label column (e.g. `"Much more important to prioritise publi"`), while the identical label is spelled out in full in the wide cross-tab table elsewhere in the same sheet. Repaired by substituting the untruncated cross-tab text for the first/last row of each overall distribution table.
- `unit="percent"` throughout - all breakdown values are plainly percentages within each group (each group's 11 categories sum to ~100).

## C19 - Satisfaction

**Source sheet:** `C19 - Satisfaction` (435 rows x 23 cols). Same ESS round/year basis: `ess_round=10`, `year="2021/22"`.

**Tables found:** five 11-point (0="Extremely dissatisfied" .. 10="Extremely satisfied") satisfaction-with-government's-COVID-19-response questions, each printed in the same 3-part pattern as the Prioritisations sheet (overall table + 3 redundant per-group tables + 1 wide cross-tab). The five topics: satisfaction with government's overall handling of COVID-19; with how health services coped; with the response for people who lost jobs/income; with the response for elderly people in care homes; with the response for families with school-age children. Unlike Prioritisations, the endpoint labels here are not truncated, so no label repair was needed.

**CSVs produced:**
- `c19_satisfaction__distribution_government_handling.csv`, `..._health_services.csv`, `..._job_income_losses.csv`, `..._elderly_care_homes.csv`, `..._school_aged_children.csv` - 11 rows each (Total N ranges 1695-1739 across the five topics).
- `c19_satisfaction__breakdown_c19_experience.csv` - 162 rows (5 questions x 11 categories x 3 groups, minus a handful of genuinely-blank source cells). `group_type="c19_experience"`, `category` prefixed with the topic slug, `unit="percent"`.

**Judgment calls / ambiguities:** none beyond the shared ESS round/year inference - all values read cleanly with no truncation, missing-header, or off-by-one issues.

## Precarity

**Source sheet:** `Precarity` (75 rows x 24 cols). A single national/rotating supplementary question, "X5: My job is secure", asked in Irish ESS rounds **2, 5 and 9** (round -> year mapping is given explicitly in the sheet itself: R2=2004, R5=2010, R9=2018 - no inference needed here, unlike the C19 sheets).

**Tables found:**
1. Rows 8-19: raw weighted frequency counts by round for 7 response categories (4 substantive: Not at all/A little/Quite/Very true, plus Not Applicable/Refusal/No Answer), with an adjacent "(%)" block that is **demonstrably broken** (e.g. round-9 "Not Applicable" shows 101.4%, and the "Total" row's own "%" cells are 247/336/203 - nowhere near 100). Only the frequency numbers were kept from this table; the broken percent block was discarded.
2. Rows 22-31: a cleanly recomputed percent-of-respondents trend, restricted to the 4 substantive categories (correctly summing to ~100% per round), plus an "Insecure" (not at all + a little true) / "Secure" (quite + very true) 2-way aggregation. Used as the primary percent trend.
3. Rows 48-63 ("Calculating Income quintile values for 2018"): a scratch/working income-**decile** breakdown for round 9 only, explicitly self-flagged by the sheet's own author as provisional ("Convert to % (and double check woith Monika results)") and containing a visible `#VALUE!` formula error plus a "Total (Valid Cases)" far short of the round-9 total N. **Excluded entirely** from the clean output due to these embedded errors.
4. Rows 66-73 ("Now quintiles"): a cleaner, apparently-final income-**quintile** breakdown of the same round-9 data (Bottom 20% / 2nd / 3rd / 4th / Top 20%), with percentages correctly summing to 1.0 per quintile and Insecure/Secure already aggregated. Used as the breakdown-by-income CSV.

**CSVs produced:**
- `precarity__trend_job_security_freq.csv` - 21 rows (7 categories x 3 rounds), `value` = weighted case count (**not** a percentage - see note above on the broken adjacent "%" block).
- `precarity__trend_job_security_percent.csv` - 18 rows (6 categories incl. Insecure/Secure x 3 rounds), `value` = percent of respondents.
- `precarity__breakdown_income_quintile_r9_2018.csv` - 30 rows (6 categories x 5 quintiles), `group_type="income_quintile"`, `unit="percent"`. Round-9/2018 only - no other round has an income cross-tab in this sheet, so the round context is encoded in the filename rather than a column (per the fixed breakdown-CSV schema).

**Judgment calls / ambiguities:**
- The raw-frequency "(%)" block adjacent to Table 1 (rows 8-19) was excluded due to the internal inconsistency described above - flagging this explicitly since it means the freq trend file has no companion percent column; use `precarity__trend_job_security_percent.csv` for percentages instead.
- The decile-level breakdown (rows 48-63) was excluded outright as unreliable/unfinished (source-acknowledged, formula error present) - only the quintile-level version (rows 66-73) was used.
- Quintile group labels normalized from the source's bare `2.0`/`3.0`/`4.0` to `"2nd quintile"`/`"3rd quintile"`/`"4th quintile"` for readability, matching the convention used elsewhere in this workbook (e.g. the Econ Sat sheet's income-quintile breakdown).
