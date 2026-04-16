-- stg_pbi_admin__capacities.sql
-- Source: Power BI Admin API — GET /admin/capacities
-- One row per Power BI Premium / Fabric capacity in the tenant.
-- Note: dlt normalises all column names to snake_case.

select
    id                              as capacity_id,
    display_name                    as capacity_name,
    sku,
    state,
    region,
    capacity_user_access_right      as access_right,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'capacities') }}
