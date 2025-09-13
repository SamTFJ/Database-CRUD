# models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Produto:
    id: Optional[int] = None
    name: str = ""
    value: float = 0.0
    quantity: int = 0
    category: Optional[str] = None
    created_at: Optional[datetime] = None

    def validate(self):
        # non-empty name
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Invalid name: must be a non-empty string.")
        # value >= 0
        try:
            val = float(self.value)
        except Exception:
            raise ValueError("Invalid value: must be numeric.")
        if val < 0:
            raise ValueError("Invalid value: must be >= 0.")
        # quantity >= 0 and an integer
        if not isinstance(self.quantity, int):
            try:
                q = int(self.quantity)
            except Exception:
                raise ValueError("Invalid quantity: must be an integer.")
            self.quantity = q
        if self.quantity < 0:
            raise ValueError("Invalid quantity: must be >= 0.")
        # category can be None or a short string
        if self.category is not None and (not isinstance(self.category, str) or len(self.category) > 80):
            raise ValueError("Invalid category: must be a string with up to 80 characters.")