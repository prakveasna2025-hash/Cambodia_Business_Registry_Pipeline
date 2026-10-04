from pathlib import Path
import requests
import pandas as pd

BASE_URL = "https://data.mef.gov.kh/api/v1/public-datasets/pd_688aee7f79fe4d000707d9b0/json"
RAW_DIR = Path("data/raw")
OUT = RAW_DIR / "new_business_registrations_api.csv"
PAGE_SIZE = 100


def fetch_all() -> list[dict]:
    """Fetch every page from the MEF API and return all items."""
    all_items: list[dict] = []
    page = 1

    while True:
        resp = requests.get(
            BASE_URL,
            params={"page": page, "page_size": PAGE_SIZE},
            timeout=30,
        )
        resp.raise_for_status()
        payload = resp.json()

        items = payload.get("items", [])
        total_pages = payload.get("total_pages", 1)
        total_items = payload.get("total_items", len(items))

        print(f"page {page}/{total_pages}: +{len(items)} rows "
              f"(running total {len(all_items) + len(items)}/{total_items})")

        all_items.extend(items)

        if page >= total_pages or not items:
            break
        page += 1

    return all_items


def save(items: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(items)
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"\nSaved {len(df)} rows -> {out}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    items = fetch_all()
    save(items, OUT)
