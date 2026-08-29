"""Generate data.csv with 5 fake fields and 10 million rows."""

import csv
import random
import time
from pathlib import Path

from faker import Faker

NUM_ROWS = 10_000_000
POOL_SIZE = 50_000
BATCH_SIZE = 50_000
EMPTY_RATE = 0.02  # ~2% of cells left blank for import-edge-case testing
OUTPUT_PATH = Path(__file__).with_name("data.csv")
FIELDS = ("name", "email", "phone", "city", "company")


def maybe_empty(value: str) -> str:
    return "" if random.random() < EMPTY_RATE else value


def main() -> None:
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    print(f"Building fake-value pool of {POOL_SIZE:,} unique-ish records...")
    names = [fake.name() for _ in range(POOL_SIZE)]
    emails = [fake.email() for _ in range(POOL_SIZE)]
    phones = [fake.phone_number() for _ in range(POOL_SIZE)]
    cities = [fake.city() for _ in range(POOL_SIZE)]
    companies = [fake.company() for _ in range(POOL_SIZE)]

    print(f"Writing {NUM_ROWS:,} rows to {OUTPUT_PATH}...")
    started = time.perf_counter()
    written = 0

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(FIELDS)

        while written < NUM_ROWS:
            size = min(BATCH_SIZE, NUM_ROWS - written)
            rows = [
                [
                    maybe_empty(names[random.randrange(POOL_SIZE)]),
                    maybe_empty(emails[random.randrange(POOL_SIZE)]),
                    maybe_empty(phones[random.randrange(POOL_SIZE)]),
                    maybe_empty(cities[random.randrange(POOL_SIZE)]),
                    maybe_empty(companies[random.randrange(POOL_SIZE)]),
                ]
                for _ in range(size)
            ]
            writer.writerows(rows)
            written += size

            elapsed = time.perf_counter() - started
            rate = written / elapsed if elapsed else 0
            print(
                f"  {written:,}/{NUM_ROWS:,} rows "
                f"({rate:,.0f} rows/s, {elapsed:.1f}s)",
                flush=True,
            )

    elapsed = time.perf_counter() - started
    print(f"Done. Wrote {written:,} rows in {elapsed:.1f}s ({written / elapsed:,.0f} rows/s).")


if __name__ == "__main__":
    main()
