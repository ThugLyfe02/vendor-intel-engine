import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import List
import pytz

from app.domain.models.transaction import Transaction


EXPECTED_HEADERS = {
    "transaction_id",
    "date",
    "vendor_name",
    "amount",
    "currency",
    "category",
    "description",
    "payment_method",
}


def load_csv(file_path: str, timezone: str = "UTC") -> List[Transaction]:
    transactions: List[Transaction] = []

    tz = pytz.timezone(timezone)

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        if not EXPECTED_HEADERS.issubset(set(reader.fieldnames or [])):
            raise ValueError("CSV headers do not match expected schema.")

        for row in reader:
            try:
                amount = Decimal(row["amount"])

                parsed_date = datetime.fromisoformat(row["date"])
                if parsed_date.tzinfo is None:
                    parsed_date = tz.localize(parsed_date)

                transaction = Transaction(
                    transaction_id=row["transaction_id"],
                    date=parsed_date,
                    vendor_raw_name=row["vendor_name"],
                    vendor_normalized_name=row["vendor_name"].strip().lower(),
                    amount=amount,
                    currency=row["currency"].upper(),
                    category=row.get("category"),
                    description=row.get("description"),
                    payment_method=row.get("payment_method"),
                )

                transactions.append(transaction)

            except (InvalidOperation, ValueError, TypeError):
                continue  # Skip malformed rows for now

    return transactions
