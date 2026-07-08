# Irish Social Attitudes 2023 — ESS Round 11 Dashboard

Interactive Streamlit companion to the UCD *Irish Social Attitudes: 2023* report
(European Social Survey, Round 11, Ireland).

## Project layout

```
ESS11 Public Report.docx.pdf         Source report (narrative + methodology)
ESS11_graphs_Ausra (version2)_20241209.xlsx   Source raw data (18 sheets, one per topic)
etl/                                 Parsers: raw xlsx -> tidy CSVs
data/processed/                      Tidy long-format CSVs consumed by the app
app/
  Home.py                            Landing page
  pages/                             One Streamlit page per topic
  utils/
    data_loader.py                   Cached CSV loading helpers
    theme.py                         Shared Plotly color/style theme
```

## Running locally

```
pip install -r requirements.txt
streamlit run app/Home.py
```

## Regenerating the data

The workbook is not tidy (print-report layout, not analysis-ready). Each script in
`etl/` reads one topic's sheet directly from the `.xlsx` and writes tidy CSVs to
`data/processed/`. Re-run all of them after any change to the source workbook:

```
for f in etl/parse_*.py; do python "$f"; done
```

See `etl/NOTES.md` for parsing decisions and any ambiguous judgment calls made per sheet.

## Deploying and embedding in WordPress

The dashboard is a standalone Streamlit app — it is **not** a WordPress plugin. The
integration path is:

1. Deploy this app somewhere Streamlit can run continuously (e.g.
   [Streamlit Community Cloud](https://streamlit.io/cloud), or any host that can run
   `streamlit run app/Home.py` behind a public URL).
2. In WordPress, add an **iframe embed** on the page/post where the dashboard should
   appear (via the Custom HTML block, or a shortcode plugin if your theme restricts
   raw HTML in posts):

   ```html
   <iframe
     src="https://<your-streamlit-app-url>/?embed=true"
     width="100%"
     height="1200"
     style="border:none;"
     loading="lazy">
   </iframe>
   ```

   The `?embed=true` query param tells Streamlit to hide its own chrome (menu, footer,
   "Deployed with Streamlit" badge) so it reads as part of the page.
3. Set the iframe height generously — Streamlit pages don't auto-resize their parent
   iframe. If the WordPress theme's content column is narrower than typical desktop
   width, test the dashboard at that width; Streamlit's layout is responsive but
   dense multi-column charts may need `layout="wide"` reconsidered for narrow embeds.
