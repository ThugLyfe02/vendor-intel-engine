import sys
import json
from decimal import Decimal

from app.ingestion.csv_loader import load_csv
from app.application.engine import VendorLeakEngine


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m app.cli <path_to_csv>")
        sys.exit(1)

    file_path = sys.argv[1]

    transactions = load_csv(file_path)

    engine = VendorLeakEngine()

    results = engine.run(transactions)

    # Convert Decimal objects to string for JSON serialization
    def decimal_serializer(obj):
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError

    print(json.dumps(results, default=decimal_serializer, indent=2))


if __name__ == "__main__":
    main()
