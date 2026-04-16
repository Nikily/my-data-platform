-- stg_pbi_admin__widely_shared_artifacts.sql
-- Source: Power BI Admin API — GET /admin/widelySharedArtifacts/linksSharedToWholeOrganization
-- One row per Power BI item shared with the whole organisation via a link.
-- dlt flattens the sharer object: sharer__displayName, sharer__emailAddress, etc.

select
    "artifactId"                            as artifact_id,
    "displayName"                           as artifact_name,
    "artifactType"                          as artifact_type,
    "accessRight"                           as access_right,
    "shareType"                             as share_type,

    -- Sharer details (flattened by dlt from the sharer object)
    "sharer__displayName"                   as sharer_display_name,
    "sharer__emailAddress"                  as sharer_email,
    "sharer__identifier"                    as sharer_identifier,
    "sharer__principalType"                 as sharer_principal_type,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'widely_shared_artifacts') }}
