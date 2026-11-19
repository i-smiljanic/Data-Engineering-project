# Retail Sales Data Pipeline

**Portfolio project | Python · Apache Airflow · PostgreSQL · SQL · pytest**

An end-to-end batch data pipeline that extracts retail sales records from CSV, validates and transforms them with Python/Pandas, and loads the results into PostgreSQL. Apache Airflow orchestrates the workflow, while pytest tests the transformation and validation logic.


## Architecture

```text
        data/raw/sales.csv
                |
                v
       extract_sales (Airflow)
                |
                v
     transform_and_validate
       Python + Pandas
                |
                v
        load_to_postgres
                |
                v
    PostgreSQL: public.sales
                |
                v
       SQL analysis queries
```

Airflow runs the tasks in order: `extract_sales >> transform_sales >> load_sales`. The source CSV is intentionally small and local so the project is easy to reproduce. In a production system, the source could be an API, object storage, or an operational database.

## What the pipeline does

1. Reads raw sales records from `data/raw/sales.csv`.
2. Checks required columns, missing values, invalid dates, non-positive quantities/prices, and duplicate transaction IDs.
3. Normalizes dates and text fields and calculates `total_amount = quantity * unit_price`.
4. Loads valid rows into PostgreSQL.
5. Uses `transaction_id` as a primary key and `ON CONFLICT` to make repeated runs idempotent (re-running does not create duplicate transactions).
6. Provides SQL examples for revenue, product and daily sales analysis.
7. Includes unit tests for transformation and validation logic.

## Repository structure

```text
data-pipeline-portfolio/
├── dags/
│   └── retail_sales_pipeline.py
├── data/
│   └── raw/
│       └── sales.csv
├── docs/
│   ├── architecture.md
│   └── interview-prep.md
├── logs/                       # created at runtime; not committed
├── plugins/                    # reserved for Airflow plugins
├── sql/
│   ├── create_tables.sql
│   └── analysis_queries.sql
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── config.py
│       ├── db.py
│       ├── extract.py
│       ├── transform.py
│       └── load.py
├── tests/
│   ├── test_transform.py
│   └── test_validation.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pytest.ini
```

## Requirements

- Docker Desktop (or Docker Engine) with Docker Compose v2
- Git
- Python 3.10+ if you want to run the unit tests outside Docker

The Airflow container uses the official Apache Airflow image. The local Compose setup is intended for learning, not production deployment.

## Run it

### 1. Configure environment

Copy `.env.example` to `.env`. The example values are for local development only; change them if you expose services or use this beyond your own machine.

### 2. Start services

From the repository root:

```bash
docker compose up airflow-init
docker compose up -d
```

The Airflow web UI is at http://localhost:8080. Login credentials are `admin` / `admin` for this local demo (created by the init service). Change them if you adapt this setup.

PostgreSQL is available on `localhost:5433` from your computer. Inside Docker, Airflow connects to the database host `warehouse` on port `5432`.

### 3. Trigger the DAG

1. Open the Airflow UI.
2. Find `retail_sales_pipeline`.
3. Unpause it if needed.
4. Click **Trigger DAG**.
5. Open the run and inspect task logs.
6. Confirm the rows were loaded:

```bash
docker compose exec warehouse psql -U pipeline_user -d retail_warehouse \
  -c "SELECT COUNT(*) FROM sales;"
```

You should see 15 records on the first successful run.

### 4. Run SQL analysis

```bash
docker compose exec warehouse psql -U pipeline_user -d retail_warehouse
```

Then run queries from `sql/analysis_queries.sql`, or execute one directly:

```sql
SELECT product, SUM(total_amount) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
```

### 5. Run tests

The test suite does not require Airflow or PostgreSQL:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
pytest -v
```

If you run tests on a machine where the Airflow provider is not installed, the tests still work because they test the independent Python transformation layer.

### 6. Stop services

```bash
docker compose down
```

To also delete the local database and Airflow metadata volumes (this permanently deletes this demo's stored data):

```bash
docker compose down -v
```

## Important implementation details

- **ETL:** extract, transform, load.
- **Orchestration:** Airflow controls task order, retries and scheduling.
- **Data quality:** required-field, type, range and duplicate checks.
- **Idempotency:** PostgreSQL upsert on `transaction_id`.
- **Separation of concerns:** DAG orchestration is separate from reusable Python business logic.
- **Testing:** pytest tests pure functions, making tests quick and independent of infrastructure.

## Limitations and possible improvements

This is a batch CSV demonstration, not a high-volume distributed system. It does not implement Spark, Kafka, NiFi, cloud object storage, secrets management, alerting, CI/CD, or production-grade observability. Good next steps:

1. Replace CSV extraction with a paginated API source.
2. Add a raw/staging table and a curated table.
3. Add data freshness and reconciliation checks.
4. Add integration tests against a disposable PostgreSQL instance.
5. Add GitHub Actions for linting and tests.
6. Add a cloud object-storage landing zone.
7. Add Kafka/Spark only if the use case requires streaming or distributed processing.
