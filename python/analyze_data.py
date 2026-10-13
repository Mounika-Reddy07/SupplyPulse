
import pandas as pd
from pathlib import Path

# Locate project files
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

input_file = DATA_DIR / "supply_chain_data.csv"
output_file = DATA_DIR / "cleaned_supply_chain_data.csv"
summary_file = DATA_DIR / "supplier_summary.csv"

# Load the generated dataset
df = pd.read_csv(input_file)

print("Original records:", len(df))

# Remove duplicate purchase orders
df = df.drop_duplicates(subset=["order_id"])

# Convert date columns
date_columns = ["order_date", "expected_delivery", "actual_delivery"]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")

# Handle missing text values
df["status"] = df["status"].fillna("Unknown")

# Calculate delivery delay for completed orders
df["delay_days"] = (
    df["actual_delivery"] - df["expected_delivery"]
).dt.days

# A delivery is on time if actual date is on or before expected date
delivered = df["status"].eq("Delivered")
df.loc[delivered, "on_time_delivery"] = (
    df.loc[delivered, "delay_days"] <= 0
).astype(int)

# Save cleaned data
df.to_csv(output_file, index=False, date_format="%Y-%m-%d")

# Create supplier performance summary
summary = df.groupby("supplier_name").agg(
    total_orders=("order_id", "count"),
    total_spend=("total_cost", "sum"),
    delayed_orders=("status", lambda x: (x == "Delayed").sum()),
    delivered_orders=("status", lambda x: (x == "Delivered").sum()),
).reset_index()

summary["total_spend"] = summary["total_spend"].round(2)

summary.to_csv(summary_file, index=False)

print("\nData cleaning completed!")
print("Cleaned dataset:", output_file)
print("Supplier summary:", summary_file)
print("\nSupplier performance:")
print(summary.to_string(index=False))
