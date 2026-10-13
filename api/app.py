
import os
from datetime import date, datetime
from decimal import Decimal
from urllib.parse import quote_plus

from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

password = os.getenv("DB_PASSWORD")

if not password:
    raise RuntimeError(
        "DB_PASSWORD environment variable is not set."
    )

encoded_password = quote_plus(password)

database_url = (
    f"mysql+pymysql://root:{encoded_password}"
    "@localhost:3306/supplypulse_db"
)

engine = create_engine(database_url, pool_pre_ping=True)


def make_json_safe(row):
    result = dict(row)

    for key, value in result.items():
        if isinstance(value, (date, datetime)):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = float(value)

    return result


@app.route("/")
def home():
    return jsonify({
        "project": "SupplyPulse",
        "message": "Supply Chain Analytics REST API",
        "endpoints": [
            "/api/orders",
            "/api/summary"
        ]
    })


@app.route("/api/orders")
def get_orders():
    with engine.connect() as connection:
        rows = connection.execute(
            text("SELECT * FROM supply_chain LIMIT 100")
        ).mappings().all()

    return jsonify([make_json_safe(row) for row in rows])


@app.route("/api/summary")
def get_summary():
    query = text("""
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(quantity), 0) AS total_quantity,
            COALESCE(SUM(total_cost), 0) AS total_cost,
            COUNT(DISTINCT supplier_id) AS total_suppliers
        FROM supply_chain
    """)

    with engine.connect() as connection:
        row = connection.execute(query).mappings().one()

    return jsonify(make_json_safe(row))


if __name__ == "__main__":
    app.run(debug=False, port=5000)
