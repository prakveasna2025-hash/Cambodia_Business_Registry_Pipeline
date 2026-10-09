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
### Day 11 — 2026-10-06 ✅
- [x] src/logging_config.py: single setup_logging(), format with module name
- [x] Every module uses log = logging.getLogger(__name__)
- [x] Replaced print() in validate.py with log.info()
- [x] Removed duplicate setup_logging() from extract.py, load.py
- [x] Error handling:
  - extract.py: ConnectionError, Timeout, non-200 → actionable RuntimeError
  - transform.py: missing raw file → FileNotFoundError with fix hint
  - load.py: missing env vars, auth fail, connection refused → clear RuntimeError
  - main.py: top-level try/except → logs error, sys.exit(1), no traceback
- [x] Tested failure path: DB stopped → clean one-line error

### Day 12 — 2026-10-07 ✅
- [x] Dockerfile: python:3.11-slim, PYTHONUNBUFFERED=1, COPY code after pip install
- [x] .dockerignore: excludes venv, .git, data, logs, docs, .env
- [x] docker-compose etl service:
  - build: .
  - depends_on postgres with service_healthy condition
  - env_file .env + environment overrides (POSTGRES_HOST=postgres, PORT=5432)
  - bind mounts ./data:/app/data and ./logs:/app/logs
- [x] Ran: docker compose up -d --build → etl Exited (0)
- [x] Data verified: 12 registry + 25 credit
- [x] Logs on host at logs/pipeline.log

### Day 13 — 2026-10-07 ✅
- [x] Installed dbt-postgres (Core 1.12.5, adapter 1.11.0)
- [x] dbt init created cambodia_dbt/ (models, macros, seeds, snapshots, tests, dbt_project.yml)
- [x] profiles.yml at project root — reads from .env via env_var()
- [x] Connection: localhost:5433, user cam_registry_dev, db cambodia_registry, schema dbt_dev
- [x] dbt debug: "All checks passed!"
- [x] No plaintext password in profile (unlike ~/.dbt/profiles.yml from init)
### Day 13 — 2026-10-07 ✅
- [x] Installed dbt-postgres (Core 1.12.5, adapter 1.11.0)
- [x] dbt init created cambodia_dbt/ (models, macros, seeds, snapshots, tests)
- [x] profiles.yml at project root — reads from .env via env_var()
- [x] Connection: localhost:5433, user cam_registry_dev, db cambodia_registry, schema dbt_dev
- [x] dbt debug: "All checks passed!"
- [x] Added .gitattributes: enforce LF line endings

### Day 14 — 2026-10-08 ✅
- [x] Deleted dbt sample models (models/example/)
- [x] sources.yml: declares raw.raw_business_registry, raw.raw_credit_by_province
- [x] stg_business_registry.sql: casts year + registration_count to INT, renames year -> registration_year
- [x] stg_credit_by_province.sql: renames credit_balance_usd_m -> credit_balance_usd_millions, credit_users_k -> credit_users_thousands
- [x] schema.yml tests (13 total) — all pass
- [x] dbt run: PASS=2; dbt test: PASS=13
- [x] Fixed accepted_values syntax (values nested under arguments)
- [x] dbt_project.yml: replaced example config with staging

### Day 15 — 2026-10-08 ✅
- [x] 3 mart models (materialized as tables):
  - mart_registrations_by_year — 3 rows (2022, 2023, 2024)
  - mart_registrations_by_company_type — 4 rows
  - mart_credit_by_area — 4 rows (Plains, Tonle Sap, Coastal, Plateau)
- [x] dbt_project.yml: marts +materialized: table
- [x] marts/schema.yml: 6 tests (unique + not_null on key of each mart)
- [x] Bug fixed: mart_registrations_by_year's CTE missed company_type
- [x] dbt run: PASS=5; dbt test: PASS=19

### Day 16 — 2026-10-08 ✅
- [x] packages.yml: dbt-labs/dbt_utils (1.4.1) for unique_combination_of_columns
- [x] staging/schema.yml updates:
  - accepted_values now uses `arguments:` wrapper (dbt 1.12 syntax)
  - not_null on reporting_year
  - dbt_utils.unique_combination_of_columns on (province, reporting_year)
- [x] tests/assert_registration_count_non_negative.sql — custom non-negative test
- [x] dbt build: PASS=26 WARN=0 ERROR=0 (5 models + 21 tests)
### Day 17 — 2026-10-09 ✅
- [x] 4 analyses in cambodia_dbt/analyses/:
  - top_province_by_credit.sql — Phnom Penh ($22.9B)
  - top5_bottom5_provinces.sql — top/bottom 5 by credit
  - pct_of_national_total.sql — % share per province (25 rows)
  - phnom_penh_vs_rest.sql — bucketed comparison with window function
- [x] Key insights:
  - Phnom Penh = 44.78% of national credit (1 province)
  - Phnom Penh = 13.8% of credit users (694k of 5.04M)
  - 24 provinces have 86% of users but only 55% of credit
### Day 19 — 2026-10-09 ✅
- [x] Complete portfolio README (190 lines)
- [x] Sections: Overview, Architecture, Data Source, Tech Stack,
      Project Structure, Setup, How to Run, Data Model, Quality Checks,
      Results, Screenshots, Limitations, Future Work, Status
- [x] Fixed broken image tag (![](docs/architecture.md) -> inline Mermaid)
- [x] Mermaid architecture diagram renders on GitHub
- [x] 5 screenshots embedded
