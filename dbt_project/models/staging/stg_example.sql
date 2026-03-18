-- Example staging model.
--
-- Staging models sit directly on top of the raw tables written by dlt.
-- Their job is to:
--   1. Select and rename columns to a consistent naming convention.
--   2. Cast types (e.g. string → timestamp).
--   3. Add lightweight filtering (e.g. exclude soft-deleted rows).
--
-- HOW TO CUSTOMISE:
--   Rename this file to match your source table, e.g. stg_orders.sql.
--   Update the source() reference to point at the dlt schema and table:
--     {{ source('raw_rest_api', 'orders') }}
--
-- Replace the query below with your actual column mapping.

with source as (
    select * from {{ source('raw_rest_api', 'orders') }}
),

renamed as (
    select
        id                                  as order_id,
        cast(created_at as timestamp)       as created_at,
        cast(updated_at as timestamp)       as updated_at,
        status                              as order_status,
        customer_id
    from source
)

select * from renamed
