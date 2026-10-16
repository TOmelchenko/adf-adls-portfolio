#!/usr/bin/env python3
"""Generate a small synthetic orders CSV for the ADF/ADLS Gen2 pipeline."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

RNG_SEED = 42
ROW_COUNT = 200
OUTPUT_PATH = Path(__file__).parent / "sample" / "orders_sample.csv"

PRODUCTS = [
    "Pallet Wrap", "Shipping Labels", "Cardboard Box - M", "Cardboard Box - L",
    "Packing Tape", "Bubble Wrap Roll", "Wooden Pallet", "Strapping Kit",
    "Barcode Scanner", "Warehouse Gloves",
]
COUNTRIES = ["DE", "NL", "BE", "PL", "FR", "AT", "CH"]
CUSTOMERS = [f"CUST-{i:04d}" for i in range(1, 41)]

START_DATE = date(2026, 1, 1)
DATE_RANGE_DAYS = 270


def generate_rows(count: int, rng: random.Random):
    for order_id in range(1, count + 1):
        order_date = START_DATE + timedelta(days=rng.randint(0, DATE_RANGE_DAYS))
        yield {
            "order_id": order_id,
            "order_date": order_date.isoformat(),
            "customer": rng.choice(CUSTOMERS),
            "product": rng.choice(PRODUCTS),
            "quantity": rng.randint(1, 50),
            "unit_price": round(rng.uniform(1.5, 120.0), 2),
            "country": rng.choice(COUNTRIES),
        }


def main():
    rng = random.Random(RNG_SEED)
    rows = list(generate_rows(ROW_COUNT, rng))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
