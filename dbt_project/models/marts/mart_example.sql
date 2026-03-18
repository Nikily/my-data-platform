-- Example mart model.
--
-- Mart models are the final analytics-ready tables consumed by Power BI.
-- They are materialised as DuckDB tables and exported as Parquet files
-- to Azure Blob Storage by the parquet_export Dagster asset.
--
-- HOW TO CUSTOMISE:
--   Rename this file to match your analytical domain, e.g. mart_sales.sql.
--   Reference staging models using ref(), not source().
--   Add the model name to MART_TABLES in pipeline/assets/export/parquet_export.py.

with orders as (
    select * from {{ ref('stg_example') }}
),

summary as (
    select
        date_trunc('day', created_at)   as order_date,
        order_status,
        count(*)                        as order_count
    from orders
    group by 1, 2
)

select * from summary
