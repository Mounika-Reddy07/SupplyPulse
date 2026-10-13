# SupplyPulse – Supply Chain Analytics

## Project Overview
SupplyPulse is a Python and MySQL-based data analytics project that analyzes supply-chain orders, supplier performance, procurement costs, and delivery status. It helps identify purchasing trends and understand supplier contributions using SQL queries and Python data analysis.

## Objectives
- Analyze supply-chain order data stored in MySQL.
- Calculate total orders, quantities, and procurement costs.
- Summarize orders by delivery status.
- Compare procurement costs across suppliers.
- Generate CSV reports for further analysis and visualization.

## Technologies Used
- **Python** – Data analysis and automation
- **MySQL** – Relational database and data storage
- **SQL** – Data retrieval and aggregation
- **Pandas** – Data manipulation and analysis
- **SQLAlchemy** – Database connectivity
- **PyMySQL** – MySQL database driver
- **Power BI** – Supply-chain dashboard and visualization

## Project Structure
```text
SupplyPulse/
├── api/
├── data/
│   ├── cleaned_supply_chain_data.csv
│   ├── delivery_summary.csv
│   ├── orders_by_status.csv
│   ├── supplier_summary.csv
│   └── supply_chain_data.csv
├── powerbi/
├── python/
├── sql/
├── analyze_supply_chain.py
└── README.md
```

## Key Features
1. Connects Python to a MySQL database.
2. Retrieves supply-chain order records using SQL.
3. Calculates total order quantity and procurement cost.
4. Analyzes orders by status.
5. Summarizes procurement costs by supplier.
6. Calculates average delivery time and total delivery delays.
7. Exports analytical summaries for reporting.

## Sample Execution Results
The project was successfully executed with the following results:

- **Total orders analyzed:** 279
- **Total quantity ordered:** 69,200
- **Total procurement cost:** 7,083,976.00
- **Suppliers analyzed:** 8

These values reflect the current dataset and may change if the data is updated.

## Prerequisites
- Python 3
- MySQL Server and MySQL Workbench
- VS Code or another Python editor
- Required Python packages: pandas, SQLAlchemy, and PyMySQL

## Database Configuration
Create the `supplypulse_db` database in MySQL and ensure that the `supply_chain` table contains the required data.

The Python script reads database credentials from environment variables rather than storing the password directly in the source code.

Configure these Windows environment variables:
- `DB_USER` – MySQL username
- `DB_PASSWORD` – MySQL password
- `DB_HOST` – MySQL server host
- `DB_PORT` – MySQL server port
- `DB_NAME` – Database name

Example values for a local development environment:
- `DB_USER`: `root`
- `DB_HOST`: `localhost`
- `DB_PORT`: `3306`
- `DB_NAME`: `supplypulse_db`

**Security:** Never upload your actual database password to GitHub.

## How to Run
1. Start MySQL Server.
2. Open the SupplyPulse project folder in VS Code.
3. Install the required packages if they are not already installed:
   ```bash
   python -m pip install pandas sqlalchemy pymysql
   ```
4. Configure the required database environment variables.
5. Ensure the `supply_chain` table contains the dataset.
6. Open the VS Code terminal in the project folder.
7. Run:
   ```bash
   python analyze_supply_chain.py
   ```

## Expected Output
The script displays:
- Total orders
- Available database columns
- Total quantity ordered
- Total procurement cost
- Order counts by status
- Procurement cost by supplier
- Delivery performance summaries

## Learning Outcomes
- Connecting Python applications to MySQL
- Writing SQL aggregation queries
- Analyzing structured business data
- Using Pandas for data processing
- Organizing data analytics projects
- Preparing data for business intelligence dashboards

## Future Enhancements
- Build interactive Power BI dashboards.
- Add supplier performance KPIs.
- Identify delayed orders and delivery trends.
- Develop an API for accessing analytical results.

## Author
Developed as a supply-chain data analytics portfolio project.
