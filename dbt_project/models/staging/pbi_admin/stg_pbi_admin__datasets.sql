-- stg_pbi_admin__datasets.sql
-- Source: Power BI Admin API — GET /admin/datasets
-- One row per dataset (semantic model) across all workspaces in the tenant.

select
    id                                              as dataset_id,
    name                                            as dataset_name,
    "configuredBy"                                  as configured_by,
    "workspaceId"                                   as workspace_id,
    "isRefreshable"                                 as is_refreshable,
    "isOnPremGatewayRequired"                       as is_on_prem_gateway_required,
    "isEffectiveIdentityRequired"                   as is_effective_identity_required,
    "isEffectiveIdentityRolesRequired"              as is_effective_identity_roles_required,
    "isInPlaceSharingEnabled"                       as is_in_place_sharing_enabled,
    "targetStorageMode"                             as target_storage_mode,
    "ContentProviderType"                           as content_provider_type,
    try_cast("createdDate" as timestamp)            as created_at,
    "webUrl"                                        as web_url,
    description,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'datasets') }}
