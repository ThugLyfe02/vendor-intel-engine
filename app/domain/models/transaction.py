from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional
import re


ISO_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


class Transaction(BaseModel):
    transaction_id: str
    date: datetime
    vendor_raw_name: str
    vendor_normalized_name: str
    amount: Decimal
    currency: str
    category: Optional[str] = None
    description: Optional[str] = None
    payment_method: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if not isinstance(v, Decimal):
            raise TypeError("Amount must be a Decimal.")
        return v

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        if not ISO_CURRENCY_PATTERN.match(v):
            raise ValueError("Currency must be a valid ISO 4217 code (e.g., 'USD').")
        return v

    @field_validator("date")
    @classmethod
    def validate_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError("Datetime must be timezone-aware.")
        return v
