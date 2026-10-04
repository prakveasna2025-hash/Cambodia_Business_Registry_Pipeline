import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("POSTGRES_USER")
pw = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5433")

url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"
print("Connecting to:", url.replace(pw, "***"))

engine = create_engine(url)

with engine.connect() as conn:
    row = conn.execute(
        text("SELECT version(), current_database(), current_user, now();")).fetchone()
    print("version:", row[0])
    print("db:     ", row[1])
    print("user:   ", row[2])
    print("time:   ", row[3])

print("\nConnection OK.")
