from transform import clean_credit, RAW_DIR, PROJECT_ROOT
from pathlib import Path
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))

REPORTING_YEAR = 2024
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "load.log"

UPSERT_SQL = text("""
    INSERT INTO raw.raw_credit_by_province
        (area, province, reporting_year, credit_balance_usd_m, credit_users_k)
    VALUES
        (:area, :province, :reporting_year, :credit_balance_usd_m, :credit_users_k)
    ON CONFLICT (province, reporting_year) DO UPDATE SET
        area = EXCLUDED.area,
        credit_balance_usd_m = EXCLUDED.credit_balance_usd_m,
        credit_users_k = EXCLUDED.credit_users_k,
        loaded_at = NOW()
""")

UPSERT_REGISTRY_SQL = text("""
    INSERT INTO raw.raw_business_registry
        (company_type, registration_count, year)
    VALUES
        (:company_type, :registration_count, :year)
    ON CONFLICT (company_type, year) DO UPDATE SET
        registration_count = EXCLUDED.registration_count,
        loaded_at = NOW()
""")


def to_registry_records(df) -> list[dict]:
    records = []
    for _, row in df.iterrows():
        records.append({
            "company_type": str(row["company_type"]),
            "registration_count": (
                int(row["registration_count"])
                if pd.notna(row["registration_count"]) else None
            ),
            "year": str(int(row["year"])),
        })
    return records


def upsert_registrations(engine, df) -> int:
    records = to_registry_records(df)
    with engine.begin() as conn:
        conn.execute(UPSERT_REGISTRY_SQL, records)
    return len(records)


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def get_engine():
    load_dotenv(PROJECT_ROOT / ".env")
    user = os.getenv("POSTGRES_USER")
    pw = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    if not all([user, pw, db]):
        raise RuntimeError("Missing POSTGRES_* env vars in .env")
    url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"
    logging.info("DB target: %s@%s:%s/%s", user, host, port, db)
    return create_engine(url)


def to_records(df, year: int) -> list[dict]:
    records = []
    for _, row in df.iterrows():
        records.append({
            "area": str(row["area"]),
            "province": str(row["province"]),
            "reporting_year": int(year),
            "credit_balance_usd_m": float(row["credit_balance_usd_m"]),
            "credit_users_k": float(row["credit_users_k"]),
        })
    return records


def upsert_credit(engine, df, year: int) -> int:
    records = to_records(df, year)
    with engine.begin() as conn:
        conn.execute(UPSERT_SQL, records)
    return len(records)


def main() -> None:
    setup_logging()
    logging.info("=== load run start ===")
    engine = get_engine()
    credit = clean_credit(RAW_DIR / "credit_by_area_province_2024.csv")
    n = upsert_credit(engine, credit, REPORTING_YEAR)
    logging.info("Upserted %d credit rows for year %d", n, REPORTING_YEAR)
    logging.info("=== load run end ===")


if __name__ == "__main__":
    main()
