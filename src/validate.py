from transform import clean_registrations, clean_credit
from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"

REQUIRED_REGISTRATIONS = ["company_type", "year"]
REQUIRED_CREDIT = ["area", "province",
                   "credit_balance_usd_m", "credit_users_k"]

NON_NEGATIVE_REGISTRATIONS = ["registration_count"]
NON_NEGATIVE_CREDIT = ["credit_balance_usd_m", "credit_users_k"]


def check_required(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    for col in cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        mask = mask | df[col].isna()
    return mask


def check_non_negative(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    for col in cols:
        if col in df.columns:
            mask = mask | (df[col] < 0).fillna(False)
    return mask


def annotate_reasons(df: pd.DataFrame, mask_required: pd.Series, mask_negative: pd.Series) -> pd.DataFrame:
    reasons = []
    for idx in df.index:
        r = []
        if mask_required.loc[idx]:
            r.append("required field null")
        if mask_negative.loc[idx]:
            r.append("negative value")
        reasons.append("; ".join(r))
    df = df.copy()
    df["reject_reason"] = reasons
    return df


def validate(name: str, df: pd.DataFrame, required: list[str], non_negative: list[str]):
    print(f"\n=== validate: {name} ===")
    print(f"input rows: {len(df)}")

    mask_required = check_required(df, required)
    mask_negative = check_non_negative(df, non_negative)
    rejected_mask = mask_required | mask_negative

    valid = df[~rejected_mask].copy()
    rejected = df[rejected_mask].copy()

    print(f"valid rows:    {len(valid)}")
    print(f"rejected rows: {len(rejected)}")

    if len(rejected) > 0:
        rejected = annotate_reasons(rejected, mask_required, mask_negative)
        REJECTED_DIR.mkdir(parents=True, exist_ok=True)
        out = REJECTED_DIR / f"{name}_rejected.csv"
        rejected.to_csv(out, index=False, encoding="utf-8")
        print(f"rejected written to: {out}")
        print(rejected.to_string())

    return valid, rejected


def main() -> None:
    reg = clean_registrations(RAW_DIR / "new_business_registrations_api.csv")
    credit = clean_credit(RAW_DIR / "credit_by_area_province_2024.csv")

    validate("registrations", reg, REQUIRED_REGISTRATIONS,
             NON_NEGATIVE_REGISTRATIONS)
    validate("credit", credit, REQUIRED_CREDIT, NON_NEGATIVE_CREDIT)


if __name__ == "__main__":
    main()
