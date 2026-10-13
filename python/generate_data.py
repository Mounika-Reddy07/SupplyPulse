import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

suppliers = [
    ("SUP001", "Alpha Components", "Electronics"),
    ("SUP002", "Bright Logistics", "Logistics"),
    ("SUP003", "Core Materials", "Raw Materials"),
    ("SUP004", "Delta Packaging", "Packaging"),
    ("SUP005", "Evergreen Supplies", "Industrial"),
    ("SUP006", "FastTrack Parts", "Automotive"),
    ("SUP007", "Global Source", "Electronics"),
    ("SUP008", "Horizon Traders", "Raw Materials"),
]

products = [
    ("PR001", "Electronic Sensor", "Electronics", 120),
    ("PR002", "Steel Sheet", "Raw Materials", 80),
    ("PR003", "Shipping Box", "Packaging", 12),
    ("PR004", "Machine Bearing", "Industrial", 45),
    ("PR005", "Circuit Board", "Electronics", 250),
    ("PR006", "Vehicle Component", "Automotive", 175),
    ("PR007", "Plastic Resin", "Raw Materials", 60),
    ("PR008", "Protective Wrap", "Packaging", 8),
]

statuses = ["Delivered", "In Transit", "Delayed", "Processing"]
weights = [55, 20, 15, 10]

output_file = DATA_DIR / "supply_chain_data.csv"
today = date.today()

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "order_id", "order_date", "supplier_id", "supplier_name",
        "product_id", "product_name", "category", "quantity",
        "unit_cost", "total_cost", "expected_delivery",
        "actual_delivery", "status", "delivery_days",
        "on_time_delivery"
    ])

    for i in range(1, 501):
        supplier = random.choice(suppliers)
        product = random.choice(products)

        order_date = today - timedelta(days=random.randint(1, 365))
        expected_delivery = order_date + timedelta(days=random.randint(5, 20))
        status = random.choices(statuses, weights=weights, k=1)[0]

        actual_delivery = ""
        delivery_days = ""
        on_time_delivery = ""

        if status == "Delivered":
            actual_date = expected_delivery + timedelta(
                days=random.randint(-4, 8)
            )
            actual_delivery = actual_date.isoformat()
            delivery_days = (actual_date - order_date).days
            on_time_delivery = int(actual_date <= expected_delivery)

        elif status == "Delayed":
            actual_delivery = ""
            delivery_days = ""
            on_time_delivery = 0

        quantity = random.randint(10, 500)
        unit_cost = product[3]
        total_cost = quantity * unit_cost

        writer.writerow([
            f"PO{i:04d}",
            order_date.isoformat(),
            supplier[0],
            supplier[1],
            product[0],
            product[1],
            product[2],
            quantity,
            unit_cost,
            total_cost,
            expected_delivery.isoformat(),
            actual_delivery,
            status,
            delivery_days,
            on_time_delivery
        ])

print("SupplyPulse dataset created successfully!")
print(f"File location: {output_file}")
print("Total purchase orders: 500")
