import hashlib
from typing import List
from app.domain.models.transaction import Transaction


def generate_dataset_hash(transactions: List[Transaction]) -> str:
    """
    Generates a deterministic SHA-256 hash of the dataset.
    """

    hasher = hashlib.sha256()

    for tx in sorted(transactions, key=lambda t: t.transaction_id):
        hasher.update(str(tx.transaction_id).encode())
        hasher.update(str(tx.date).encode())
        hasher.update(str(tx.vendor_normalized_name).encode())
        hasher.update(str(tx.amount).encode())
        hasher.update(str(tx.currency).encode())

    return hasher.hexdigest()
