import sys, logging
from minidb import *

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")

db = Database("demo")

users = (TableBuilder("users")
         .add_column("id", IntegerType(), primary_key=True, nullable=False)
         .add_column("name", StringType(50), nullable=False)
         .build(db))

orders = db.create_table_with_factory("orders", {
    "columns": [
        {"name": "id", "type": "int", "nullable": False, "primary_key": True},
        {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "id")},
        {"name": "product", "type": "string", "nullable": False, "max_length": 100},
        {"name": "price", "type": "int", "nullable": False}
    ]
})

users.insert({"id": 1, "name": "Alice"}, db=db)
users.insert({"id": 2, "name": "Bob"}, db=db)

orders.insert({"id": 100, "user_id": 1, "product": "Book", "price": 300}, db=db)
orders.insert({"id": 101, "user_id": 1, "product": "Lamp", "price": 500}, db=db)
orders.insert({"id": 102, "user_id": 2, "product": "Pen", "price": 20}, db=db)

print("Запит >100, price↓, select id/product:")
for r in (SimpleQuery(orders)
          .where("price", ">", 100)
          .order_by("price", ascending=False)
          .select(["id","product"])
          .execute()):
    print(r.to_dict())

print("JOIN orders×users:")
for r in JoinedTable(orders, users, "user_id", "id").rows():
    print(r.data)

print("Сума:", SimpleQuery(orders).sum("price"), "Середнє:", SimpleQuery(orders).avg("price"))

try:
    with db.transaction():
        orders.insert({"id": 999, "user_id": 999, "product": "X", "price": 1}, db=db)
except Exception as e:
    print("Очікуваний відкат транзакції:", e)
