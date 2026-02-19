import re


COMMON_SUFFIXES = [
    "inc",
    "llc",
    "ltd",
    "corp",
    "co",
    "company",
    "corporation",
]


class VendorNormalizer:

    @staticmethod
    def normalize(name: str) -> str:
        if not name:
            raise ValueError("Vendor name cannot be empty.")

        normalized = name.lower()

        # Remove punctuation
        normalized = re.sub(r"[^\w\s]", "", normalized)

        # Remove common corporate suffixes
        tokens = normalized.split()
        tokens = [t for t in tokens if t not in COMMON_SUFFIXES]

        # Collapse spaces
        normalized = " ".join(tokens)
        normalized = re.sub(r"\s+", " ", normalized)

        return normalized.strip()
