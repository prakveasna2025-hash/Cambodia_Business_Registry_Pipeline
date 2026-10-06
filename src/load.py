from logging_config import setup_logging
from transform import clean_credit, RAW_DIR, PROJECT_ROOT
from pathlib import Path
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.exc import OperationalError

log = logging.getLogger(__name__)

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


def get_engine():
    load_dotenv(PROJECT_ROOT / ".env")
    user = os.getenv("POSTGRES_USER")
    pw = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")

    missing = [k for k, v in {
        "POSTGRES_USER": user,
        "POSTGRES_PASSWORD": pw,
        "POSTGRES_DB": db,
    }.items() if not v]
    if missing:
        raise RuntimeError(
            f"Missing env vars in .env: {', '.join(missing)}. "
            f"Check {PROJECT_ROOT / '.env'}."
        )

    url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"
    log.info("DB target: %s@%s:%s/%s", user, host, port, db)

    engine = create_engine(url)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as e:
        msg = str(e).lower()
        if "password" in msg or "authentication" in msg:
            raise RuntimeError(
                f"DB auth failed for user '{user}'. "
                f"Check POSTGRES_USER / POSTGRES_PASSWORD in .env."
            ) from e
        if "could not connect" in msg or "connection refused" in msg:
            raise RuntimeError(
                f"Cannot connect to Postgres at {host}:{port}. "
                f"Is the DB running? Try: docker compose ps"
            ) from e
        raise RuntimeError(
            f"DB connection failed: {e}. "
            f"Target: {user}@{host}:{port}/{db}"
        ) from e

    return engine


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
    log.info("=== load run start ===")
    engine = get_engine()
    credit = clean_credit(RAW_DIR / "credit_by_area_province_2024.csv")
    n = upsert_credit(engine, credit, REPORTING_YEAR)
    log.info("Upserted %d credit rows for year %d", n, REPORTING_YEAR)
    log.info("=== load run end ===")


if __name__ == "__main__":
    main()
