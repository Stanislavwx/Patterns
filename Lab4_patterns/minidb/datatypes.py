from __future__ import annotations
from datetime import date, datetime
from typing import Any, Optional

class DataType:
    py_types: tuple[type, ...] = (object,)

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        return isinstance(value, self.py_types)

    def normalize(self, value: Any) -> Any:
        return value

class IntegerType(DataType):
    py_types = (int,)

class StringType(DataType):
    def __init__(self, max_length: Optional[int] = None) -> None:
        self.max_length = max_length

    py_types = (str,)

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        return self.max_length is None or len(value) <= self.max_length

class BooleanType(DataType):
    py_types = (bool,)

class DateType(DataType):
    py_types = (date, datetime)

    def normalize(self, value: Any) -> Any:
        if isinstance(value, datetime):
            return value.date()
        return value
