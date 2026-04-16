-- stg_pbi_admin__refreshables.sql
-- Source: Power BI Admin API — GET /admin/capacities/refreshables
-- One row per dataset that has been refreshed or has a refresh schedule (7-day window).
-- dlt flattens nested objects with __ separator:
--   lastRefresh__* columns come from the lastRefresh object
--   capacity__*  columns come from the capacity object
--   group__*     columns come from the group object
-- configuredBy is a string array — dlt creates a child table refreshables__configured_by

select
    id                                              as refreshable_id,
    name                                            as refreshable_name,
    kind,

    -- Refresh window
    try_cast("startTime" as timestamp)              as window_start_at,
    try_cast("endTime"   as timestamp)              as window_end_at,

    -- Refresh stats
    "refreshCount"                                  as refresh_count,
    "refreshFailures"                               as refresh_failure_count,
    "averageDuration"                               as avg_duration_seconds,
    "medianDuration"                                as median_duration_seconds,
    "refreshesPerDay"                               as refreshes_per_day,

    -- Last refresh (flattened by dlt)
    "lastRefresh__refreshType"                      as last_refresh_type,
    try_cast("lastRefresh__startTime" as timestamp) as last_refresh_started_at,
    try_cast("lastRefresh__endTime"   as timestamp) as last_refresh_ended_at,
    "lastRefresh__status"                           as last_refresh_status,
    "lastRefresh__requestId"                        as last_refresh_request_id,

    -- Associated capacity (flattened by dlt)
    "capacity__id"                                  as capacity_id,
    "capacity__displayName"                         as capacity_name,
    "capacity__sku"                                 as capacity_sku,

    -- Associated workspace (flattened by dlt)
    "group__id"                                     as group_id,
    "group__name"                                   as group_name,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'refreshables') }}
