# Data Dictionary — Cambodia Business Registry Pipeline

Last updated: 2026-10-04

---

## Dataset 1: New Business Registrations (2022–2024)

**Source:** MEF Open Data Portal
**API endpoint:** https://data.mef.gov.kh/api/v1/public-datasets/pd_688aee7f79fe4d000707d9b0/json
**Fetch script:** src/fetch_api.py
**Local cache:** data/raw/new_business_registrations_api.csv (gitignored)

### Fetch metadata
- Last fetched: 2026-10-05
- HTTP response size: 1226 bytes (1.20 KB)
- CSV file size: 428 bytes
- Rows: 12
- Pages: 1 (page_size=100)

### Grain
One row per company type per year.

### Primary key
Composite: (`new_business_registration`, `year`)
Verified: 0 duplicate (company_type, year) pairs across 12 rows.

### Columns

| Column | Type (raw) | Type (target) | Nullable | Description | Example |
|---|---|---|---|---|---|
| new_business_registration | string | string | No | Company type. Values: Partnership Company, Sole Proprietorship, Foreign Trade Company, Capital Company | Sole Proprietorship |
| number_of_registration | string or null | integer | Yes | Number of new registrations for that company type in that year. Null = not reported (NOT zero). | "5910" |
| year | float | integer | No | Reporting year. Range 2022–2024. | 2022.0 |

### Known issues
- `number_of_registration` arrives as string in the API. Cast with `pd.to_numeric(..., errors="coerce")`.
- `year` arrives as float. Cast to int.
- Partnership Company has nulls for 2022 and 2023. Confirmed true nulls via API (not zeros). Do not impute.
- Sole Proprietorship fell from 7,066 (2023) to 4,750 (2024). Flag to verify 2024 completeness.

---

## Dataset 2: Credit Distribution by Area and Province (2024)

**Source:** MEF Open Data Portal (manual download)
**Local cache:** data/raw/credit_by_area_province_2024.csv (gitignored)

### Fetch metadata
- Source type: manual download
- File size: 881 bytes
- Rows: 25

### Grain
One row per province, single reporting year 2024.
Verified: 25 rows, 0 duplicate provinces.

### Primary key
(`Province`)

### Columns

| Column | Type (raw) | Type (target) | Nullable | Description | Example |
|---|---|---|---|---|---|
| Area | string | string | No | Regional grouping. Values: Plains, Plateau, Tonle Sap, Coastal | Plains |
| Province | string | string | No | Province name (English). 25 unique values incl. Phnom Penh. | Kandal |
| Total_Credit_Balance_million_usd | float | float | No | Total outstanding credit balance, millions of USD. | 2994.5 |
| Total_Credit_User_thousand | float | float | No | Number of credit users, thousands. | 393.9 |

### Known issues
- No year column. Dataset represents 2024 only (per title). Add year as constant if needed downstream.
- Units embedded in column names. Consider renaming during clean: `credit_balance_usd_m`, `credit_users_k`.

---

## Cross-Dataset Notes
- Registrations data is national, aggregated by company type and year.
- Credit data is provincial, single year.
- Different grains — do not join directly.