import requests
import json

URL = "https://data.mef.gov.kh/api/v1/public-datasets/pd_688aee7f79fe4d000707d9b0/json"


def main():
    resp = requests.get(URL, params={"page": 1, "page_size": 10}, timeout=30)
    print("Status:", resp.status_code)
    print("Content-Type:", resp.headers.get("Content-Type"))
    print("Raw (first 2000 chars):")
    print(resp.text[:2000])

    try:
        data = resp.json()
        print("\n=== TOP-LEVEL KEYS ===")
        print(list(data.keys()) if isinstance(data, dict) else type(data))

        print("\n=== PRETTY JSON (first 3000 chars) ===")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
    except Exception as e:
        print("JSON parse failed:", e)


if __name__ == "__main__":
    main()
