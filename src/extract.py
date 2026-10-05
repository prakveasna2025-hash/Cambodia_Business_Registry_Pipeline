from pathlib import Path
import logging
import requests
import pandas as pd

BASE_URL = "https://data.mef.gov.kh/api/v1/public-datasets/pd_688aee7f79fe4d000707d9b0/json"
RAW_DIR = Path("data/raw")
OUT = RAW_DIR / "new_business_registrations_api.csv"
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "fetch.log"
PAGE_SIZE = 100


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


def fetch_all() -> list[dict]:
    all_items: list[dict] = []
    page = 1

    while True:
        resp = requests.get(
            BASE_URL,
            params={"page": page, "page_size": PAGE_SIZE},
            timeout=30,
        )
        resp.raise_for_status()

        size_bytes = len(resp.content)
        size_kb = size_bytes / 1024
        server_size = resp.headers.get("Content-Length", "n/a")

        payload = resp.json()
        items = payload.get("items", [])
        total_pages = payload.get("total_pages", 1)
        total_items = payload.get("total_items", len(items))

        logging.info(
            "page %d/%d | response: %d bytes (%.2f KB) | server Content-Length: %s | rows this page: %d",
            page, total_pages, size_bytes, size_kb, server_size, len(items),
        )

        all_items.extend(items)

        if page >= total_pages or not items:
            break
        page += 1

    logging.info("Total rows fetched: %d (API reported total_items=%d)", len(
        all_items), total_items)
    return all_items


def save(items: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(items)
    df.to_csv(out, index=False, encoding="utf-8")

    file_bytes = out.stat().st_size
    logging.info("Saved CSV: %s | %d rows | %d bytes (%.2f KB)",
                 out, len(df), file_bytes, file_bytes / 1024)


def main() -> None:
    setup_logging()
    logging.info("=== extract run start ===")
    items = fetch_all()
    save(items, OUT)
    logging.info("=== extract run end ===")


if __name__ == "__main__":
    main()
