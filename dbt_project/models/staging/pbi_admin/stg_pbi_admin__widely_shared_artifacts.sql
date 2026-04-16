-- stg_pbi_admin__widely_shared_artifacts.sql
-- Source: Power BI Admin API — GET /admin/widelySharedArtifacts/linksSharedToWholeOrganization
-- One row per Power BI item shared with the whole organisation via a link.
-- Note: dlt normalises all column names to snake_case and flattens the
--       sharer object with __ separator.
-- Guard: if the API returned no records dlt will not have created the table yet;
--        the if  block returns an empty result set in that case.

{% set relation = adapter.get_relation(
    database = 'platform',
    schema   = 'raw_pbi_admin',
    identifier = 'widely_shared_artifacts'
) %}

{% if relation %}

select
    artifact_id,
    display_name                    as artifact_name,
    artifact_type,
    access_right,
    share_type,
    sharer__display_name            as sharer_display_name,
    sharer__email_address           as sharer_email,
    sharer__identifier              as sharer_identifier,
    sharer__principal_type          as sharer_principal_type,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'widely_shared_artifacts') }}

{% else %}

select
    null::varchar   as artifact_id,
    null::varchar   as artifact_name,
    null::varchar   as artifact_type,
    null::varchar   as access_right,
    null::varchar   as share_type,
    null::varchar   as sharer_display_name,
    null::varchar   as sharer_email,
    null::varchar   as sharer_identifier,
    null::varchar   as sharer_principal_type,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
