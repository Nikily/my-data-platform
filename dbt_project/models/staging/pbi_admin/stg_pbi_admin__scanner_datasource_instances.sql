-- stg_pbi_admin__scanner_datasource_instances.sql
-- Source: top-level datasourceInstances from the Workspace Scanner API result.
-- One row per unique datasource instance across all scanned workspaces.
-- Linked to datasets via stg_pbi_admin__scanner_datasets__datasource_usages.
-- Note: connection_details is flattened by dlt with __ separator.
--       Most fields are null for datasource types that don't use them
--       (e.g. Excel has path but no server; SQL has server+database but no path).

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_datasource_instances'
) %}

{% if relation %}

select
    datasource_id,
    datasource_type,
    gateway_id,

    -- Relational (SQL, Analysis Services, etc.)
    connection_details__server      as server,
    connection_details__database    as database,

    -- File-based (Excel, CSV, SharePoint, etc.)
    connection_details__path        as file_path,
    connection_details__url         as url,

    -- Other connection detail fields (present for some source types)
    connection_details__account     as account,
    connection_details__domain      as domain,
    connection_details__kind        as kind,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_datasource_instances') }}

{% else %}

select
    null::varchar   as datasource_id,
    null::varchar   as datasource_type,
    null::varchar   as gateway_id,
    null::varchar   as server,
    null::varchar   as database,
    null::varchar   as file_path,
    null::varchar   as url,
    null::varchar   as account,
    null::varchar   as domain,
    null::varchar   as kind,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
