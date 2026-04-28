# 🚀 Tech Stack

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![Dagster](https://img.shields.io/badge/Dagster-5C6AC4?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-2D6CDF?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)


This project is a production-style ETL pipeline that migrates data from SQLite to PostgreSQL using Dagstar orchestration.
It demonstrates a complete data engineering workflow including:
🧹 Data extraction from SQLite
🔄 Transformation & cleaning using Pandas
✅ Data validation using Pydantic
🏗️ Schema modeling with SQLAlchemy
🚀 Automated loading into PostgreSQL
📊 Fully orchestrated workflows with Dagstar
Built to simulate real-world business data migration pipelines used in modern data platforms.


🧠 #Business Value

This pipeline solves key enterprise problems:
📦 Data Migration → Move legacy SQLite data into scalable PostgreSQL
🧹 Data Cleaning → Remove inconsistencies before loading
🔍 Data Validation → Ensure schema correctness using Pydantic
⚙️ Automation → Fully scheduled and repeatable ETL workflows
📈 Scalability Ready → Designed for production expansion (S3, BigQuery, etc.)


.
├── data/                  # Raw and versioned datasets (CSV, SQLite DB)
├── localdb/              # Local JSON mock database layer
├── src/                  # Core ETL pipeline
│   ├── fetch_db.py       # Extract data from SQLite
│   ├── transform_data.py # Data cleaning & transformation
│   ├── validate_*.py     # Pydantic validation layers
│   ├── models.py         # SQLAlchemy ORM models
│   ├── load_to_Db.py     # Load data into PostgreSQL
│   ├── main.py           # Airflow DAG definition
│   └── save_raw_csv.py   # Raw data archival
├── tests/                # Unit tests for data sources
├── requirements.txt      # Dependencies
└── README.md

Tool
Purpose
Dagstar
Workflow orchestration 
🐼 Pandas
Data transformation & cleaning
🧩 SQLAlchemy
Database ORM & PostgreSQL integration
📦 Pydantic
Schema validation & data integrity
🐘 PostgreSQL
Target data warehouse
🗃️ SQLite
Source transactional Database

🔄 ETL Pipeline Flow
Extract
Pull data from SQLite database (sales.db)
Transform
Clean missing values
Normalize schemas
Format timestamps & IDs
Validate
Enforce schema rules using Pydantic
Validate customers, orders, products separately
Load
Insert processed data into PostgreSQL using SQLAlchemy
Orchestrate
Dagstar manages the entire orcastration Pipeline


Covers:
SQLite extraction validation
PostgreSQL load verification
Schema validation logic


python -m venv venv
source venv/bin/activate   # Linux/Mac
# OR
venv\Scripts\activate      # Windows

git clone https://github.com/<your-username>/etl-sqlite-postgres-airflow.git
cd etl-sqlite-postgres-airflow

pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/dbname"
export AIRFLOW_HOME=$PWD/airflow
airflow db init
airflow dags test etl_sqlite_pipeline 2026-04-27

pytest tests/




📊 Key Features
🔁 Incremental ETL-ready design
🧠 Strict data validation (Pydantic)
🏗️ ORM-based schema control (SQLAlchemy)
⚡ DAGSTAR orchestration
📦 Modular and scalable architecture
🧪 Test-driven pipeline reliability


📈 Future Improvements
🔄 Add incremental watermarking
☁️ Migrate to cloud (GCP BigQuery / AWS RDS)
📡 Add monitoring (DAGSTAR cloud)
🧠 Integrate ML-based data anomaly detection

👨‍💻 Author
Shamola Nassan
Data Engineering | ETL Systems | Python Automation | DAGSTAR pipelines
