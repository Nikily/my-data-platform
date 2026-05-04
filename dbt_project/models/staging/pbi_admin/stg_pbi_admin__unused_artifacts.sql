-- stg_pbi_admin__unused_artifacts.sql
-- Source: Power BI Admin API — GET /admin/groups/{groupId}/unused
-- One row per artifact (dataset, report, or dashboard) not accessed in 30+ days.
-- group_id is added by the ingestion asset so each row can be joined back to groups.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'unused_artifacts'
) %}

{% if relation %}

select
    "artifactId"                                    as artifact_id,
    "displayName"                                   as artifact_name,
    "artifactType"                                  as artifact_type,
    "artifactSizeInMB"                              as artifact_size_mb,
    group_id                                        as workspace_id,
    try_cast("createdDateTime"      as timestamp)   as created_at,
    try_cast("lastAccessedDateTime" as timestamp)   as last_accessed_at,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'unused_artifacts') }}

{% else %}

select
    null::varchar   as artifact_id,
    null::varchar   as artifact_name,
    null::varchar   as artifact_type,
    null::double    as artifact_size_mb,
    null::varchar   as workspace_id,
    null::timestamp as created_at,
    null::timestamp as last_accessed_at,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
