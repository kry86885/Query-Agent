import sqlite3

# Create SQLite DB in memory (change ":memory:" to "mydb.db" to save to file)
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# --- Create Tables ---
cursor.execute("""
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    country TEXT
)
""")

cursor.execute("""
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
)
""")

cursor.execute("""
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE OrderItems (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
)
""")

# --- Insert Sample Data ---
# Customers
cursor.executemany("""
INSERT INTO Customers (name, email, country)
VALUES (?, ?, ?)
""", [
    ("Alice Johnson", "alice@example.com", "USA"),
    ("Bob Smith", "bob@example.com", "Canada"),
    ("Charlie Brown", "charlie@example.com", "UK"),
    ("Diana Prince", "diana@example.com", "Germany"),
    ("Ethan Hunt", "ethan@example.com", "Australia"),
])

# Products
cursor.executemany("""
INSERT INTO Products (product_name, price, category)
VALUES (?, ?, ?)
""", [
    ("Laptop", 1200.50, "Electronics"),
    ("Smartphone", 800.00, "Electronics"),
    ("Desk Chair", 150.75, "Furniture"),
    ("Headphones", 99.99, "Electronics"),
    ("Coffee Mug", 12.50, "Kitchen"),
])

# Orders
cursor.executemany("""
INSERT INTO Orders (customer_id, order_date)
VALUES (?, ?)
""", [
    (1, "2024-01-10"),
    (2, "2024-02-15"),
    (3, "2024-03-20"),
    (4, "2024-04-25"),
    (5, "2024-05-30"),
])

# Order Items
cursor.executemany("""
INSERT INTO OrderItems (order_id, product_id, quantity)
VALUES (?, ?, ?)
""", [
    (1, 1, 1),   # Alice buys 1 Laptop
    (1, 5, 2),   # Alice buys 2 Coffee Mugs
    (2, 2, 1),   # Bob buys 1 Smartphone
    (3, 3, 1),   # Charlie buys 1 Desk Chair
    (4, 4, 3),   # Diana buys 3 Headphones
])

conn.commit()

# --- Verify Data ---
for table in ["Customers", "Products", "Orders", "OrderItems"]:
    print(f"\n{table}:")
    for row in cursor.execute(f"SELECT * FROM {table}"):
        print(row)