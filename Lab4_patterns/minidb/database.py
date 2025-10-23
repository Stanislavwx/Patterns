from __future__ import annotations
from typing import Dict, Optional
from .core import Table, Column
from .datatypes import *
import json
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    _instance: Optional['Database'] = None

    def __new__(cls, name: str="default"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name: str="default"):
        if getattr(self, "_initialized", False):
            return
        self.name = name
        self.tables: Dict[str, Table] = {}
        self._initialized = True

    def register_table(self, table: Table) -> Table:
        self._check_foreign_keys(table)
        if table.name in self.tables:
            raise ValueError(f"Table {table.name} already exists")
        self.tables[table.name] = table
        logger.info("Table ready: %s", table.name)
        return table

    def get_table(self, name: str) -> Optional[Table]:
        return self.tables.get(name)

    def _check_foreign_keys(self, table: Table) -> None:
        for col in table.columns.values():
            if col.foreign_key:
                ref_table, ref_col = col.foreign_key
                t = self.tables.get(ref_table)
                if t is None or ref_col not in t.columns:
                    raise ValueError(f"Foreign key references unknown {ref_table}.{ref_col}")

    def create_table_with_factory(self, name: str, schema: dict) -> Table:
        types = {"int": IntegerType, "string": StringType, "bool": BooleanType, "date": DateType}
        cols: list[Column] = []
        for c in schema.get("columns", []):
            typ = c["type"]
            if typ not in types:
                raise ValueError(f"Unknown type {typ}")
            dt = types[typ](c["max_length"]) if types[typ] is StringType and "max_length" in c else types[typ]()
            cols.append(Column(
                name=c["name"],
                data_type=dt,
                nullable=c.get("nullable", True),
                primary_key=c.get("primary_key", False),
                foreign_key=tuple(c["foreign_key"]) if c.get("foreign_key") else None,
            ))
        return self.register_table(Table(name, cols))

    def to_json(self) -> str:
        return json.dumps({"name": self.name, "tables": {n: t.to_dict() for n, t in self.tables.items()}}, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, s: str) -> 'Database':
        payload = json.loads(s)
        db = cls(payload.get("name", "loaded"))
        db.tables.clear()
        type_map = {"IntegerType": IntegerType, "StringType": StringType, "BooleanType": BooleanType, "DateType": DateType}
        for name, td in payload["tables"].items():
            cols = []
            for c in td["columns"]:
                tcls = type_map[c["type"]]
                dt = tcls(c["meta"]) if tcls is StringType and c.get("meta") else tcls()
                cols.append(Column(
                    name=c["name"],
                    data_type=dt,
                    nullable=c["nullable"],
                    primary_key=c["primary_key"],
                    foreign_key=tuple(c["foreign_key"]) if c["foreign_key"] else None,
                ))
            table = Table(name, cols); table.next_id = td["next_id"]
            for r in td["rows"]:
                rid = r.get("_id"); d = {k: v for k, v in r.items() if k != "_id"}
                row = table.insert(d, db=None); row.id = rid
            db.tables[name] = table
        return db

    @contextmanager
    def transaction(self):
        snapshot = self.to_json()
        logger.info("TX begin")
        try:
            yield self
            logger.info("TX commit")
        except Exception:
            loaded = Database.from_json(snapshot)
            self.tables = loaded.tables
            logger.info("TX rollback")
            raise

class TableBuilder:
    def __init__(self, name: str):
        self.name = name
        self._columns: list[Column] = []

    def add_column(self, name: str, data_type: DataType, *, nullable: bool=True,
                   primary_key: bool=False, foreign_key: Optional[tuple[str, str]]=None) -> 'TableBuilder':
        self._columns.append(Column(name, data_type, nullable, primary_key, foreign_key))
        return self

    def build(self, db: Database) -> Table:
        table = Table(self.name, self._columns)
        return db.register_table(table)
