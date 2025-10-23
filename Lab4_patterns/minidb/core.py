from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from .database import Database
from dataclasses import dataclass
from .datatypes import DataType
import logging


logger = logging.getLogger(__name__)

@dataclass
class Column:
    name: str
    data_type: DataType
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[Tuple[str, str]] = None

    def validate(self, value: Any) -> bool:
        if value is None:
            return self.nullable
        return self.data_type.validate(value)

@dataclass
class Row:
    data: Dict[str, Any]
    id: Optional[int] = None

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def keys(self) -> Iterable[str]:
        return self.data.keys()

    def to_dict(self) -> Dict[str, Any]:
        out = dict(self.data)
        out["_id"] = self.id
        return out

class Table:
    def __init__(self, name: str, columns: Iterable[Column]) -> None:
        self.name = name
        self.columns: Dict[str, Column] = {c.name: c for c in columns}
        self.rows: List[Row] = []
        self.next_id: int = 1
        if sum(1 for c in self.columns.values() if c.primary_key) > 1:
            raise ValueError(f"Table {self.name}: only one primary key allowed")

    def insert(self, row_data: Dict[str, Any], db: Optional['Database']=None) -> Row:
        for column in self.columns.values():
            value = row_data.get(column.name)
            if not column.validate(value):
                raise ValueError(f"Invalid value for column {column.name}: {value}")
            if value is not None:
                row_data[column.name] = column.data_type.normalize(value)

        for c in self.columns.values():
            if c.primary_key:
                new_pk_val = row_data.get(c.name)
                if new_pk_val is not None:
                    for r in self.rows:
                        if r[c.name] == new_pk_val:
                            raise ValueError(f"Duplicate primary key value for {c.name}: {new_pk_val}")

        if db is not None:
            for col in self.columns.values():
                if col.foreign_key and row_data.get(col.name) is not None:
                    ref_table, ref_col = col.foreign_key
                    t = db.get_table(ref_table)
                    if t is None or ref_col not in t.columns:
                        raise ValueError(f"Invalid foreign key reference {ref_table}.{ref_col}")
                    target = row_data[col.name]
                    if not any(rr[ref_col] == target for rr in t.rows):
                        raise ValueError(f"Foreign key value {target} not found in {ref_table}.{ref_col}")

        row = Row(dict(row_data))
        row.id = self.next_id
        self.next_id += 1
        self.rows.append(row)
        return row

    def update(self, predicate, updates: Dict[str, Any]) -> int:
        count = 0
        for row in self.rows:
            if predicate(row):
                for k, v in updates.items():
                    col = self.columns.get(k)
                    if col is None:
                        raise KeyError(f"Column {k} not found")
                    if not col.validate(v):
                        raise ValueError(f"Invalid value for {k}: {v}")
                    row[k] = col.data_type.normalize(v)
                count += 1
        return count

    def delete(self, predicate) -> int:
        before = len(self.rows)
        self.rows = [r for r in self.rows if not predicate(r)]
        return before - len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "columns": [
                {
                    "name": c.name,
                    "type": c.data_type.__class__.__name__,
                    "nullable": c.nullable,
                    "primary_key": c.primary_key,
                    "foreign_key": c.foreign_key,
                    "meta": getattr(c.data_type, "max_length", None),
                } for c in self.columns.values()
            ],
            "rows": [r.to_dict() for r in self.rows],
            "next_id": self.next_id,
        }

class SimpleQuery:
    def __init__(self, table: Table) -> None:
        self.table = table
        self.selected_columns: Optional[List[str]] = None
        self.filter_conditions: List[tuple] = []
        self.sort_column: Optional[str] = None
        self.sort_ascending: bool = True

    def select(self, columns: List[str]) -> 'SimpleQuery':
        self.selected_columns = columns
        return self

    def where(self, column: str, operator: str, value: Any) -> 'SimpleQuery':
        self.filter_conditions.append((column, operator, value))
        return self

    def order_by(self, column: str, ascending: bool=True) -> 'SimpleQuery':
        self.sort_column = column
        self.sort_ascending = ascending
        return self

    def _matches(self, row: Row) -> bool:
        for column, operator, value in self.filter_conditions:
            rv = row[column]
            if operator == "=" and rv != value:
                return False
            elif operator == ">" and not (rv is not None and rv > value):
                return False
            elif operator == "<" and not (rv is not None and rv < value):
                return False
            elif operator == ">=" and not (rv is not None and rv >= value):
                return False
            elif operator == "<=" and not (rv is not None and rv <= value):
                return False
            elif operator == "!=" and not (rv != value):
                return False
            elif operator == "contains":
                if rv is None or value is None or str(value) not in str(rv):
                    return False
        return True

    def execute(self) -> List[Row]:
        filtered = [r for r in self.table if self._matches(r)]
        if self.sort_column:
            filtered.sort(
                key=lambda r: (r[self.sort_column] is None, r[self.sort_column]),
                reverse=not self.sort_ascending,
            )
        results: List[Row] = []
        for r in filtered:
            if self.selected_columns:
                data = {c: r[c] for c in self.selected_columns if c in r.keys()}
                nr = Row(data); nr.id = r.id
                results.append(nr)
            else:
                results.append(r)
        logger.info("Query %s: %d rows", self.table.name, len(results))
        return results

    def count(self) -> int:
        return len(self.execute())

    def sum(self, column: str) -> float:
        vals = [r[column] for r in self.execute() if isinstance(r[column], (int, float))]
        return float(sum(vals))

    def avg(self, column: str) -> float:
        vals = [r[column] for r in self.execute() if isinstance(r[column], (int, float))]
        return float(sum(vals)) / len(vals) if vals else 0.0

class JoinedTable:
    def __init__(self, left: Table, right: Table, left_key: str, right_key: str) -> None:
        self.left = left; self.right = right
        self.left_key = left_key; self.right_key = right_key

    def rows(self) -> List[Row]:
        right_index = {}
        for r in self.right.rows:
            right_index.setdefault(r[self.right_key], []).append(r)
        out: List[Row] = []
        for l in self.left.rows:
            for r in right_index.get(l[self.left_key], []):
                merged = dict(l.data)
                for k, v in r.data.items():
                    merged[k if k not in merged else f"{self.right.name}.{k}"] = v
                out.append(Row(merged))
        logger.info("Join %s.%s=%s.%s: %d rows", self.left.name, self.left_key, self.right.name, self.right_key, len(out))
        return out
