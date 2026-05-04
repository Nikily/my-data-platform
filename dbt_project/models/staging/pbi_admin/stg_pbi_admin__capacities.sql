-- stg_pbi_admin__capacities.sql
-- Source: Power BI Admin API — GET /admin/capacities
-- One row per Power BI Premium / Fabric capacity in the tenant.
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'capacities'
) %}

{% if relation %}

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

{% else %}

select
    null::varchar as capacity_id,
    null::varchar as capacity_name,
    null::varchar as sku,
    null::varchar as state,
    null::varchar as region,
    null::varchar as access_right,
    null::varchar as _dlt_load_id,
    null::varchar as _dlt_id
where 1 = 0

{% endif %}
