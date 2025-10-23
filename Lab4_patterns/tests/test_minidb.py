import unittest
from minidb import *

class TestMiniDB(unittest.TestCase):
    def setUp(self):
        Database._instance = None  # type: ignore
        self.db = Database("test")

        users = (TableBuilder("users")
                 .add_column("id", IntegerType(), primary_key=True, nullable=False)
                 .add_column("name", StringType(50), nullable=False)
                 .build(self.db))

        self.db.create_table_with_factory("orders", {
            "columns": [
                {"name": "id", "type": "int", "nullable": False, "primary_key": True},
                {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "id")},
                {"name": "product", "type": "string", "nullable": False, "max_length": 100},
                {"name": "price", "type": "int", "nullable": False}
            ]
        })

        users.insert({"id": 1, "name": "Alice"}, db=self.db)
        users.insert({"id": 2, "name": "Bob"}, db=self.db)

        orders = self.db.get_table("orders")
        orders.insert({"id": 100, "user_id": 1, "product": "Book", "price": 300}, db=self.db)
        orders.insert({"id": 101, "user_id": 2, "product": "Pen", "price": 20}, db=self.db)
        orders.insert({"id": 102, "user_id": 1, "product": "Lamp", "price": 500}, db=self.db)

    def test_fk_enforced(self):
        orders = self.db.get_table("orders")
        with self.assertRaises(ValueError):
            orders.insert({"id": 103, "user_id": 999, "product": "X", "price": 10}, db=self.db)

    def test_query(self):
        orders = self.db.get_table("orders")
        q = SimpleQuery(orders).where("price", ">", 100).order_by("price", ascending=False)
        rows = q.execute()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["product"], "Lamp")

    def test_join(self):
        users = self.db.get_table("users")
        orders = self.db.get_table("orders")
        jt = JoinedTable(orders, users, "user_id", "id")
        rows = jt.rows()
        self.assertEqual(len(rows), 3)
        sample = rows[0].data
        self.assertIn("name", sample)

    def test_aggregates(self):
        orders = self.db.get_table("orders")
        q = SimpleQuery(orders)
        self.assertEqual(q.count(), 3)
        self.assertAlmostEqual(q.sum("price"), 820.0)
        self.assertAlmostEqual(q.avg("price"), round(820.0/3, 10))

    def test_json_save_load(self):
        s = self.db.to_json()
        Database._instance = None  # reset
        loaded = Database.from_json(s)
        self.assertIn("users", loaded.tables)
        self.assertIn("orders", loaded.tables)
        self.assertEqual(len(loaded.get_table("orders").rows), 3)
