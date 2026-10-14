# Prompt: Kenya Secondary Schools Atlas

Paste everything below the line into Google Antigravity (agent mode) or Claude. The `data/` folder in this project already holds clean data, so the agent does not need to scrape anything.

---

You are a senior GIS and front-end engineer. Build and extend an interactive web atlas of secondary schools in Kenya's 47 counties. Work inside the current project folder.

## Inputs (already in this folder)
- `data/kenya_secondary_schools_by_county_2020.csv` and `data/kenya_secondary_2020.json`: one row per county (47 rows). Source: Ministry of Education, *Basic Education Statistical Booklet 2020*, Annex III tables III.1 to III.13.
  Fields: `county, code, public_schools, private_schools, total_schools, enrol_public, enrol_private, enrol_total, boys_public, girls_public, gpi, ger, ner, transition, teachers_tsc, teachers_bom, teachers_private, teachers_total, str_public, str_private, str_all, computers, internet_pct, area_km2, avg_school_size, schools_per_1000km2, private_share`.
- `data/kenya_counties.geojson`: 47 county polygons in WGS84. Each feature has `properties.code` (1 to 47, the official county code). Join on `code`, not on the name.
- `index.html`: the current working atlas (Leaflet 1.9.4 + Chart.js 4.4.1, data embedded inline). Use it as the baseline and keep everything that works.

National reference values (2020): 10,390 schools (9,100 public, 1,290 private), 3,569,279 students, GER 76.5%, NER 54.1%, transition 87.1%, GPI 1.01, student-teacher ratio 28, schools with internet 34.0%.

## Must keep
1. A choropleth of all 47 counties. Clicking a county highlights its outline and opens a side panel with schools (public/private split), students, teachers, students per school, and bars for GER, NER, transition, students per teacher, internet % and GPI, each with a tick for the national average.
2. A layer switcher (total, public, private, students, GER, students per teacher, private %, internet %, GPI), each with its own colour ramp, 7 quantile classes and a legend.
3. Hover tooltips, county search with keyboard navigation, reset view, an optional basemap toggle.
4. A ranking bar chart for the active layer, a public vs private donut, a schools vs GER bubble chart coloured by former province, a GPI bar chart, and a sortable table of all counties. Clicking any chart bar, bubble or table row selects that county on the map.
5. Light and dark themes, mobile layout (no horizontal scroll at 400 px), visible keyboard focus.

## Add these features
1. **Compare mode**: pick two counties and show their indicators side by side with a difference column.
2. **Export**: download the current table as CSV and the current map view as PNG.
3. **Sub-county drill-down**: if `data/subcounties.geojson` exists, clicking a county loads its sub-counties. Otherwise show "Sub-county data not loaded".
4. **School points layer**: if `data/schools.csv` exists (columns `name, lat, lon, type, county`), cluster the points with Leaflet.markercluster and colour public schools green and private schools purple.
5. **Priority index**: a 0 to 100 score per county combining low GER, high students per teacher, low GPI and low internet access (equal weights, min-max scaled). Add it as a map layer and list the top 10 priority counties.
6. **Narrative tab**: a short auto-generated paragraph for the selected county ("Garissa has 68 secondary schools, 48.5% of them private...").

## Engineering rules
- One self-contained `index.html` plus the `data/` folder; load libraries from cdnjs with pinned versions; no build step.
- Fetch the GeoJSON and CSV from `data/` when served over http, and fall back to the inline copies when opened as `file://`.
- Run `python3 -m http.server 8000` and test in the browser. Fix every console error before finishing.
- Keep the colour tokens defined on `:root` with dark-mode overrides.
- Cite the source in the footer.

## Deliverables
1. Updated `index.html`.
2. `CHANGELOG.md` listing what changed.
3. A short test checklist confirming that every feature above works on desktop and mobile widths.
