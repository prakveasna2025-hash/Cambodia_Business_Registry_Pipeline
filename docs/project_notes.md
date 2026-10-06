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
## How to Resume (environment)

1. Open terminal in C:\Projects\Cambodia_Business_Registry_Pipeline
2. Activate venv: venv\Scripts\activate
3. Start DB: docker compose up -d
4. Confirm DB healthy: docker compose ps
5. Confirm schema: docker exec -it cambodia_registry_pg psql -U cam_registry_dev -d cambodia_registry -c "\dt raw.*"

## Current State (last updated: 2026-10-04, end of Day 5)
- DB user: cam_registry_dev
- DB: cambodia_registry
- Host port: 5433
- Tables: raw.raw_business_registry
- Raw CSVs cached in data/raw/ (gitignored)
- No data loaded into Postgres yet
- Next: Day 6

## Day 6 Candidates
- sql/02_create_raw_credit.sql (credit table)
- src/clean.py (cleaning layer: cast types, rename cols)
- Load layer: push cleaned data into Postgres

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

### Day 6 — 2026-10-05 ✅
- [x] Added logging to src/fetch_api.py (file + console)
- [x] Logs: response bytes, Content-Length header, row count per page
- [x] Log file: logs/fetch.log (gitignored)
- [x] Recorded fetch metadata in data_dictionary.md
- [x] Registrations: 1226 bytes response / 428 bytes CSV / 12 rows
- [x] Credit CSV: 881 bytes / 25 rows
### Day 7 — 2026-10-05 ✅
- [x] Renamed src/fetch_api.py -> src/extract.py
- [x] Removed src/test_api.py, src/test_db.py
- [x] Filled src/transform.py: snake_case + semantic renames + province standardization
- [x] Registrations: registration_count + year = Int64; 2 true nulls preserved
- [x] Credit: 25 rows, no nulls, province names standardized
- [x] Note: pandas 3.0 uses `str` dtype for text (replaces `object`)

### Day 8 — 2026-10-05 ✅
- [x] src/validate.py: check_required, check_non_negative, annotate_reasons, validate
- [x] Rejects written to data/rejected/<name>_rejected.csv with reject_reason column
- [x] Paths anchored to PROJECT_ROOT (Path(__file__).resolve().parents[1]) — runs from anywhere
- [x] Test: injected 3 bad rows → 3 caught (1 null, 2 negative)
- [x] Real data: 12 + 25 rows, 0 rejects (clean)
### Day 9 — 2026-10-06 ✅
- [x] sql/02_create_raw_credit.sql: raw.raw_credit_by_province
  - UNIQUE (province, reporting_year) — enables UPSERT
  - NUMERIC for money/counts (exact decimal, not FLOAT)
- [x] src/load.py: UPSERT via INSERT ... ON CONFLICT ... DO UPDATE
  - Credentials from .env via os.getenv (never hardcoded)
  - Transaction via engine.begin() — all-or-nothing
- [x] Proven idempotent: ran twice → still 25 rows
- [x] Proven overwrite: tampered Kandal → upsert reverted it
### Day 10 — 2026-10-06 ✅
- [x] sql/03_registry_unique.sql: UNIQUE (company_type, year) on raw.raw_business_registry
- [x] src/load.py: upsert_registrations() with ON CONFLICT DO UPDATE
- [x] main.py: full pipeline (extract → transform → validate → load)
- [x] Reordered imports: PROJECT_ROOT + sys.path.insert BEFORE local imports
- [x] .vscode/settings.json: disable formatOnSave + organizeImports (keeps sys.path trick working)
- [x] Idempotency proven: ran twice → 12 registry + 25 credit, unchanged
