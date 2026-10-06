from pathlib import Path
import sys
import logging

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from extract import fetch_all, save, setup_logging as extract_logging, OUT as RAW_OUT
from transform import clean_registrations, clean_credit, RAW_DIR
from validate import (
    validate,
    REQUIRED_REGISTRATIONS, REQUIRED_CREDIT,
    NON_NEGATIVE_REGISTRATIONS, NON_NEGATIVE_CREDIT,
)
from load import (
    get_engine, upsert_credit, upsert_registrations,
    setup_logging as load_logging,
    REPORTING_YEAR,
)



def main() -> None:
    extract_logging()
    logging.info("=== PIPELINE START ===")

    # 1. EXTRACT
    logging.info("[1/4] extract: fetching registrations")
    items = fetch_all()
    save(items, RAW_OUT)

    # 2. TRANSFORM
    logging.info("[2/4] transform: cleaning datasets")
    reg = clean_registrations(RAW_DIR / "new_business_registrations_api.csv")
    credit = clean_credit(RAW_DIR / "credit_by_area_province_2024.csv")

    # 3. VALIDATE
    logging.info("[3/4] validate")
    reg_valid, _ = validate("registrations", reg,
                            REQUIRED_REGISTRATIONS, NON_NEGATIVE_REGISTRATIONS)
    credit_valid, _ = validate(
        "credit", credit, REQUIRED_CREDIT, NON_NEGATIVE_CREDIT)

    # 4. LOAD
    logging.info("[4/4] load")
    engine = get_engine()
    n_reg = upsert_registrations(engine, reg_valid)
    n_credit = upsert_credit(engine, credit_valid, REPORTING_YEAR)
    logging.info("Upserted registrations: %d rows", n_reg)
    logging.info("Upserted credit:        %d rows", n_credit)

    logging.info("=== PIPELINE END ===")


if __name__ == "__main__":
    main()
