# Project Notes — Cambodia Business Registry Pipeline

## Project Goal
A data pipeline that ingests, cleans, and stores Cambodian business registry data for analysis and querying. Built as a learning + portfolio project.

## Repo
- Local: C:\Projects\Cambodia_Business_Registry_Pipeline
- Remote: https://github.com/prakveasna2025-hash/Cambodia_Business_Registry_Pipeline
- Branch: main

## Tech Stack
- Python 3.x (venv in ./venv)
- pandas, requests, pytest, python-dotenv
- SQL + Docker (planned)

## Folder Layout
src/     – pipeline code
test/    – unit tests
data/    – raw/ and processed/ (gitignored except .gitkeep)
sql/     – SQL schemas/queries
logs/    – runtime logs (gitignored)
docs/    – notes and docs
main.py  – entry point

## Progress Log

### Day 1 — 2026-10-03 ✅
- Created GitHub repo, cloned locally
- Folder structure: src, test, data/raw, data/processed, sql, logs, docs
- Python venv created, activated, gitignored
- requirements.txt pinned
- .gitignore, README, Dockerfile stub, docker-compose stub

### Day 2 — 2026-10-04 (in progress)
- [ ] Open dataset/API page
- [ ] Download raw CSV into data/raw/
- [ ] Inspect with pandas (columns, types, nulls)
- [ ] Record findings below

## Data Source
- Source URL: <TBD>
- Download method: direct CSV (planned)
- File: data/raw/registry.csv (planned)

## Data Findings (from pandas inspection)
- Rows: 
- Columns: 
- Nulls:
- Dtype issues:
- Encoding issues:
- Duplicates:

## Open Questions / TODO
- Confirm exact dataset URL
- Decide CSV vs API (leaning CSV)
- Add Dockerfile content when Docker work begins

## Conventions
- Commit messages: "Day N: <short summary>"
- One commit per day minimum
- Never commit: venv/, data/raw/*, data/processed/*, .env, logs/*
### Dataset 2 (live source): new_business_registrations
- API: https://data.mef.gov.kh/api/v1/public-datasets/pd_688aee7f79fe4d000707d9b0/json
- Pagination: ?page=N&page_size=100
- Response shape: { items: [...], total_items, page, page_size, total_pages }
- Fields: new_business_registration (str), number_of_registration (str|null), year (float)
- Quirks:
  - number_of_registration arrives as string, must cast to numeric
  - year arrives as float, cast to int
  - Partnership Company nulls for 2022 & 2023 are TRUE nulls (confirmed in API)
- Local cache: data/raw/new_business_registrations_api.csv (gitignored)
- Fallback CSV: new_business_registrations_2022_2024.csv (manual export, matches API)
### Day 2 — 2026-10-04 ✅
- [x] Identified MEF open data portal as source
- [x] Manual CSV: new_business_registrations_2022_2024.csv
- [x] Manual CSV: credit_by_area_province_2024.csv
- [x] API tested: pd_688aee7f79fe4d000707d9b0 (12 rows, 1 page w/ page_size=100)
- [x] API fetcher written: src/fetch_api.py (paginated)
- [x] Raw API output cached: data/raw/new_business_registrations_api.csv

### Day 3 — 2026-10-04 ✅
- [x] Confirmed grain for both datasets
- [x] Confirmed columns + primary keys
- [x] Wrote docs/data_dictionary.md
- [x] Committed + pushed

### Day 4 — 2026-10-04 ✅
- [x] docker-compose.yml: postgres:16-alpine service
- [x] Named volume: cambodia_business_registry_pipeline_pg_data
- [x] Host port 5433 (5432 used by other project)
- [x] Connection test: src/test_db.py → OK
- [x] Persistence test: table survived container removal
- [x] Committed + pushed
### Day 5 — 2026-10-04 ✅
- [x] DB user changed: cam_registry_dev (was pipeline)
- [x] sql/01_create_raw_schema.sql: schema raw + raw_business_registry
- [x] Applied via: Get-Content file | docker exec -i ... psql
- [x] Table confirmed: raw.raw_business_registry