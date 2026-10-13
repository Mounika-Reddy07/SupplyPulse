
import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text


# ==========================================
# SupplyPulse - Supply Chain Analytics
# ==========================================

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# ==========================================
# Database Configuration
# ==========================================

DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "supplypulse_db"

if not DB_PASSWORD:
    raise ValueError(
        "DB_PASSWORD is not set. "
        "Set the Windows environment variable and restart VS Code."
    )


# Build the MySQL connection URL safely
encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ==========================================
# Read Data from MySQL
# ==========================================

def load_supply_chain_data():
    query = text("SELECT * FROM supply_chain")

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    if df.empty:
        raise ValueError(
            "The supply_chain table is empty. "
            "Import your CSV data into MySQL first."
        )

    return df


# ==========================================
# Analyze Supply Chain Data
# ==========================================

def analyze_data(df):
    print("\n========== SupplyPulse Analytics ==========")
    print(f"Total orders: {len(df)}")

    print("\nColumns available:")
    print(", ".join(df.columns.astype(str)))

    # Total quantity
    if "quantity" in df.columns:
        total_quantity = pd.to_numeric(
            df["quantity"], errors="coerce"
        ).sum()

        print(f"\nTotal quantity ordered: {total_quantity:,.0f}")

    # Total procurement cost
    if "total_cost" in df.columns:
        total_cost = pd.to_numeric(
            df["total_cost"], errors="coerce"
        ).sum()

        print(f"Total procurement cost: {total_cost:,.2f}")

    # Order status summary
    if "status" in df.columns:
        print("\nOrders by status:")

        status_summary = (
            df.groupby("status", dropna=False)
            .size()
            .reset_index(name="total_orders")
            .sort_values("total_orders", ascending=False)
        )

        print(status_summary.to_string(index=False))

        status_summary.to_csv(
            DATA_DIR / "orders_by_status.csv",
            index=False
        )

    # Supplier cost summary
    if {"supplier_name", "total_cost"}.issubset(df.columns):
        supplier_summary = df.copy()

        supplier_summary["total_cost"] = pd.to_numeric(
            supplier_summary["total_cost"],
            errors="coerce"
        )

        supplier_summary = (
            supplier_summary.groupby("supplier_name", dropna=False)
            .agg(
                total_orders=("supplier_name", "size"),
                procurement_cost=("total_cost", "sum")
            )
            .reset_index()
            .sort_values("procurement_cost", ascending=False)
        )

        print("\nProcurement cost by supplier:")
        print(supplier_summary.to_string(index=False))

        supplier_summary.to_csv(
            DATA_DIR / "supplier_summary.csv",
            index=False
        )

    # Delivery performance
    if "delivery_days" in df.columns:
        delivery_days = pd.to_numeric(
            df["delivery_days"], errors="coerce"
        )

        print("\nDelivery performance:")
        print(
            f"Average delivery days: "
            f"{delivery_days.mean():.1f}"
        )

        if "status" in df.columns:
            delivery_summary = df.copy()

            delivery_summary["delivery_days"] = delivery_days

            delivery_summary = (
                delivery_summary.groupby("status", dropna=False)
                .agg(
                    total_orders=("status", "size"),
                    average_delivery_days=("delivery_days", "mean")
                )
                .reset_index()
            )

            delivery_summary["average_delivery_days"] = (
                delivery_summary["average_delivery_days"].round(1)
            )

            print(delivery_summary.to_string(index=False))

            delivery_summary.to_csv(
                DATA_DIR / "delivery_summary.csv",
                index=False
            )

    # Save a copy of the data used for analysis
    df.to_csv(DATA_DIR / "supply_chain_data.csv", index=False)

    print("\nAnalysis completed successfully.")
    print(f"Output files saved in: {DATA_DIR}")


# ==========================================
# Main Program
# ==========================================

def main():
    try:
        print("Connecting to the SupplyPulse database...")

        df = load_supply_chain_data()

        analyze_data(df)

    except Exception as error:
        print("\nSupplyPulse could not complete the analysis.")
        print(f"Error: {error}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
