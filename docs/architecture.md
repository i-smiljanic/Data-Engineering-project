# Architecture and design notes

## Pipeline stages

| Stage | Responsibility | Implementation |
|---|---|---|
| Extract | Read source records | `extract_sales()` reads CSV |
| Validate | Reject records violating rules | `validate_sales()` |
| Transform | Standardize values and derive measures | `transform_sales()` |
| Load | Persist records | PostgreSQL `INSERT ... ON CONFLICT` |
| Orchestrate | Run stages in order and retry failures | Airflow DAG |

## Why separate orchestration from business logic?

Airflow should coordinate when tasks run and how they depend on one another. Python modules contain the reusable extraction, validation, transformation and loading logic. This separation makes the logic easier to test without starting Airflow.

## Why use a primary key and upsert?

`transaction_id` identifies a transaction. A primary key prevents duplicate IDs in the target table. `ON CONFLICT ... DO UPDATE` makes a rerun safe and allows changed source values to update the existing row. This is an example of idempotent loading for this dataset.

## Why PostgreSQL?

It is a relational database with SQL support, constraints, indexes and transactions. It is suitable for demonstrating structured analytical data storage. It is not being presented as a distributed data warehouse.

## Data-quality rules

- Required columns must exist.
- Dataset must not be empty.
- Required values cannot be null.
- Transaction IDs must be unique within the input batch.
- Dates must parse.
- Quantity must be a positive number.
- Unit price must be numeric and non-negative.

## Airflow behavior

The DAG defines three PythonOperator tasks and dependencies. The DAG is scheduled daily, does not backfill old intervals (`catchup=False`), and retries failed tasks twice with a two-minute delay.

## Production considerations

For production, avoid passing large datasets through Airflow XCom. Store intermediate data in object storage or a database and pass only a URI or batch identifier. Use a secrets backend rather than committed credentials. Add structured logs, alerting, data freshness checks, schema evolution strategy, CI/CD, and integration tests. Define retention, access control, backup and recovery policies.
