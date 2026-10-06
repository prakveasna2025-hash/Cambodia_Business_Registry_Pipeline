import logging
from pathlib import Path
import re
import pandas as pd

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROVINCE_MAP = {
    "Steung Traeng": "Stung Treng",
    "Sihanoukville": "Preah Sihanouk",
    "Tbong Khmum": "Tboung Khmum",
}

COLUMN_RENAME = {
    "new_business_registration": "company_type",
    "number_of_registration": "registration_count",
    "total_credit_balance_million_usd": "credit_balance_usd_m",
    "total_credit_user_thousand": "credit_users_k",
}


def to_snake(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip())
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s)
    s = re.sub(r"_+", "_", s).strip("_").lower()
    return s


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={c: to_snake(c) for c in df.columns})
    df = df.rename(
        columns={k: v for k, v in COLUMN_RENAME.items() if k in df.columns})
    return df


def standardize_province(value):
    if pd.isna(value):
        return value
    s = re.sub(r"\s+", " ", str(value).strip())
    return PROVINCE_MAP.get(s, s)


def clean_registrations(path: Path) -> pd.DataFrame:

    if not path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {path}. "
            f"Run extract first: python src/extract.py"
        )
    
    df = pd.read_csv(path)
    df = standardize_columns(df)
    df["registration_count"] = pd.to_numeric(
        df["registration_count"], errors="coerce").astype("Int64")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    return df


def clean_credit(path: Path) -> pd.DataFrame:

    if not path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {path}. "
            f"Make sure credit_by_area_province_2024.csv is in data/raw/."
        )
    
    df = pd.read_csv(path)
    df = standardize_columns(df)
    df["province"] = df["province"].apply(standardize_province)
    return df


def preview(name: str, df: pd.DataFrame) -> None:
    print(f"\n=== {name} ===")
    print(f"shape: {df.shape}")
    print("dtypes:")
    print(df.dtypes.to_string())
    print("head:")
    print(df.head().to_string())
    print("nulls:")
    print(df.isna().sum().to_string())


def main() -> None:
    reg = clean_registrations(RAW_DIR / "new_business_registrations_api.csv")
    credit = clean_credit(RAW_DIR / "credit_by_area_province_2024.csv")
    preview("registrations", reg)
    preview("credit", credit)


if __name__ == "__main__":
    main()
