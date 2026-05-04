-- stg_pbi_admin__refreshables.sql
-- Source: Power BI Admin API — GET /admin/capacities/refreshables
-- One row per dataset with a refresh history or active schedule (7-day window).
-- Note: dlt normalises all column names to snake_case and flattens nested
--       objects with __ separator (e.g. last_refresh__status).

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'refreshables'
) %}

{% if relation %}

select
    id                                              as refreshable_id,
    name                                            as refreshable_name,
    kind,

    -- Refresh window
    try_cast(start_time as timestamp)               as window_start_at,
    try_cast(end_time   as timestamp)               as window_end_at,

    -- Refresh stats
    refresh_count,
    refresh_failures                                as refresh_failure_count,
    average_duration                                as avg_duration_seconds,
    median_duration                                 as median_duration_seconds,
    refreshes_per_day,

    -- Last refresh (flattened by dlt)
    last_refresh__refresh_type                      as last_refresh_type,
    try_cast(last_refresh__start_time as timestamp) as last_refresh_started_at,
    try_cast(last_refresh__end_time   as timestamp) as last_refresh_ended_at,
    last_refresh__status                            as last_refresh_status,
    last_refresh__request_id                        as last_refresh_request_id,

    -- Associated capacity (flattened by dlt)
    capacity__id                                    as capacity_id,
    capacity__display_name                          as capacity_name,
    capacity__sku                                   as capacity_sku,

    -- Associated workspace (flattened by dlt)
    group__id                                       as group_id,
    group__name                                     as group_name,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'refreshables') }}

{% else %}

select
    null::varchar   as refreshable_id,
    null::varchar   as refreshable_name,
    null::varchar   as kind,
    null::timestamp as window_start_at,
    null::timestamp as window_end_at,
    null::bigint    as refresh_count,
    null::bigint    as refresh_failure_count,
    null::double    as avg_duration_seconds,
    null::double    as median_duration_seconds,
    null::double    as refreshes_per_day,
    null::varchar   as last_refresh_type,
    null::timestamp as last_refresh_started_at,
    null::timestamp as last_refresh_ended_at,
    null::varchar   as last_refresh_status,
    null::varchar   as last_refresh_request_id,
    null::varchar   as capacity_id,
    null::varchar   as capacity_name,
    null::varchar   as capacity_sku,
    null::varchar   as group_id,
    null::varchar   as group_name,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
