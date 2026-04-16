-- stg_pbi_admin__capacities.sql
-- Source: Power BI Admin API — GET /admin/capacities
-- One row per Power BI Premium / Fabric capacity in the tenant.
-- Note: admins is a string array — dlt creates a child table raw_pbi_admin.capacities__admins

select
    id                                      as capacity_id,
    "displayName"                           as capacity_name,
    sku,
    state,
    region,
    "capacityUserAccessRight"               as access_right,
    "tenantKeyId"                           as tenant_key_id,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'capacities') }}
