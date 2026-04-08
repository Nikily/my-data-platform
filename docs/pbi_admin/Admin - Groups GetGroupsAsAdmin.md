---
layout: Reference
title: Admin - Groups GetGroupsAsAdmin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/groups-get-groups-as-admin
uid: api.powerbi.com.power-bi.admin.groups_getgroupsasadmin
breadcrumb_path: /rest/breadcrumb/toc.json
rest_product: Power BI
ms.service: powerbi
products:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
author: rloutlaw
ms.author: routlaw
ms.devlang: rest-api
ms.date: 2018-03-14T00:00:00.0000000Z
uhfHeaderId: MSDocsHeader-MSPowerBI
feedback_system: None
enable_rest_try_it: true
ms.topic: generated-reference
description: Returns a list of workspaces for the organization. Permissions The user must be a Fabric administrator or authenticate using a service principal.
locale: en-us
document_id: c78f6176-f36b-285d-f2df-df53dc1eff19
document_version_independent_id: bb05357b-1f68-5431-bf99-a3005a72a65b
updated_at: 2026-03-16T22:05:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Groups-Get-Groups-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/126d8a75bf5d035e45ba75d3656a5f82fcc0c9b5/docs-ref-autogen/power-bi/Admin/Groups-Get-Groups-As-Admin.yml
git_commit_id: 126d8a75bf5d035e45ba75d3656a5f82fcc0c9b5
site_name: Docs
depot_name: MSDN.powerbi-rest-api
page_type: rest
page_kind: operation
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.powerbi-rest-api/{branchName}{pdfName}
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-bi/admin/groups-get-groups-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Groups-Get-Groups-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 356a542b-eff1-fcc6-c3e7-5152a4792783
---

# Admin - Groups GetGroupsAsAdmin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of workspaces for the organization.

## Permissions

- The user must be a Fabric administrator or authenticate using a service principal.
- Delegated permissions are supported.

When running under service prinicipal authentication, an app **must not** have any admin-consent required premissions for Power BI set on it in the Azure portal.

## Required Scope

Tenant.Read.All or Tenant.ReadWrite.All

Relevant only when authenticating via a standard delegated admin access token. Must not be present when authentication via a service principal is used.

## Limitations

Maximum 50 requests per hour or 15 requests per minute, per tenant. This call will also time out after 30 seconds to prevent adverse effect on the Power BI service. 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$top={$top}
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand={$expand}&$filter={$filter}&$top={$top}&$skip={$skip}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| $top | query | True | integer (int32)<br>minimum: 1maximum: 5000 | Returns only the first n results. This parameter is mandatory and must be in the range of 1-5000. |
| $expand | query |  | string | Accepts a comma-separated list of data types, which will be expanded inline in the response. Supports `users`, `reports`, `dashboards`, `datasets`, `dataflows`, and `workbooks`. |
| $filter | query |  | string | Returns a subset of a results based on [Odata](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptions) filter query parameter condition. |
| $skip | query |  | integer (int32) | Skips the first n results. Use with top to fetch results beyond the first 5000. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdminGroups | OK |

## Examples

| Get deleted workspaces example. |
| --- |
| Get orphaned workspaces example. |
| Get workspaces with their 'dashboards' expanded example |
| Get workspaces with their 'datasets' expanded example |
| Get workspaces with their 'datasets' expanded example. |
| Get workspaces with their 'reports' expanded example |
| Get workspaces with their 'users' expanded example. |
| Get workspaces with their 'workbooks' expanded example |

### Get deleted workspaces example.

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$filter=state eq 'Deleted'&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "183dcf10-47b8-48c4-84aa-f0bf9d5f8fcf",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "name": "Sample Group 2",
      "description": "Deleted sample group",
      "type": "Workspace",
      "state": "Deleted"
    }
  ]
}
```

### Get orphaned workspaces example.

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=users&$filter=(not users/any()) or (not users/any(u: u/groupUserAccessRight eq Microsoft.PowerBI.ServiceContracts.Api.GroupUserAccessRight'Admin'))&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "d5caa808-8c91-400a-911d-06af08dbcc31",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "name": "Orphaned Group",
      "description": "Sample orphan group",
      "type": "Workspace",
      "state": "Active",
      "hasWorkspaceLevelSettings": false,
      "users": []
    }
  ]
}
```

### Get workspaces with their 'dashboards' expanded example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=dashboards&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "94E57E92-CEE2-486D-8CC8-218C97200579",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "capacityMigrationStatus": "Migrated",
      "description": "shorter description",
      "type": "Workspace",
      "state": "Removing",
      "name": "a",
      "hasWorkspaceLevelSettings": false,
      "dashboards": [
        {
          "id": "4668133c-ae3f-42fb-ad7c-214a8623280c",
          "displayName": "SQlAzure-Refresh.pbix",
          "isReadOnly": false
        },
        {
          "id": "a8f18ca7-63e8-4220-bc1c-f576ec180b98",
          "displayName": "cdvc",
          "isReadOnly": false
        }
      ]
    }
  ]
}
```

### Get workspaces with their 'datasets' expanded example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=datasets&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "94E57E92-CEE2-486D-8CC8-218C97200579",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "capacityMigrationStatus": "Migrated",
      "description": "shorter description",
      "type": "Workspace",
      "state": "Removing",
      "name": "a",
      "hasWorkspaceLevelSettings": false,
      "datasets": [
        {
          "id": "8ce96c50-85a0-4db3-85c6-7ccc3ed46523",
          "name": "SQlAzure-Refresh",
          "addRowsAPIEnabled": false,
          "configuredBy": "admin@granularcontrols.ccsctp.net",
          "isRefreshable": true,
          "isEffectiveIdentityRequired": false,
          "isEffectiveIdentityRolesRequired": false,
          "isOnPremGatewayRequired": false,
          "targetStorageMode": "Abf",
          "createdDate": "2019-04-30T21:35:15.867-07:00",
          "ContentProviderType": "PbixInImportMode",
          "isInPlaceSharingEnabled": false
        },
        {
          "id": "7d6a4f72-1906-4e08-a469-bd6bc1ab7b69",
          "name": "NESGames",
          "addRowsAPIEnabled": false,
          "configuredBy": "admin@granularcontrols.ccsctp.net",
          "isRefreshable": true,
          "isEffectiveIdentityRequired": false,
          "isEffectiveIdentityRolesRequired": false,
          "isOnPremGatewayRequired": false,
          "targetStorageMode": "Abf",
          "createdDate": "2019-04-30T21:35:15.867-07:00",
          "ContentProviderType": "PbixInImportMode",
          "isInPlaceSharingEnabled": false
        }
      ]
    }
  ]
}
```

### Get workspaces with their 'datasets' expanded example.

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=datasets
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "e380d1d0-1fa6-460b-9a90-1a5c6b02414c",
      "isReadOnly": false,
      "isOnDedicatedCapacity": true,
      "capacityId": "0f084df7-c13d-451b-af5f-ed0c466403b2",
      "defaultDatasetStorageFormat": "Small",
      "name": "Sample Group 1",
      "description": "Sample group",
      "type": "Workspace",
      "state": "Active",
      "hasWorkspaceLevelSettings": true,
      "datasets": [
        {
          "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "name": "SalesMarketing",
          "addRowsAPIEnabled": false,
          "configuredBy": "john@contoso.com",
          "isRefreshable": true,
          "isEffectiveIdentityRequired": false,
          "isEffectiveIdentityRolesRequired": false,
          "isOnPremGatewayRequired": false,
          "isInPlaceSharingEnabled": false,
          "encryption": {
            "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "encryptionStatus": "InSyncWithWorkspace"
          }
        }
      ]
    },
    {
      "id": "183dcf10-47b8-48c4-84aa-f0bf9d5f8fcf",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "name": "Sample Group 2",
      "description": "Deleted sample group",
      "type": "Workspace",
      "state": "Deleted",
      "datasets": []
    }
  ]
}
```

### Get workspaces with their 'reports' expanded example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=reports&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "EC1EE11F-845D-495E-82A3-9DAC2072305A",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "capacityMigrationStatus": "Migrated",
      "description": "cvcv",
      "type": "Workspace",
      "state": "Active",
      "name": "WSv2Test12",
      "hasWorkspaceLevelSettings": true,
      "reports": []
    },
    {
      "id": "94E57E92-CEE2-486D-8CC8-218C97200579",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "capacityMigrationStatus": "Migrated",
      "description": "shorter description",
      "type": "Workspace",
      "state": "Removing",
      "name": "a",
      "hasWorkspaceLevelSettings": false,
      "reports": [
        {
          "id": "5DBA60B0-D9A7-42AE-B12C-6D9D51E7739A",
          "reportType": "PowerBIReport",
          "name": "SQlAzure-Refresh",
          "datasetId": "8ce96c50-85a0-4db3-85c6-7ccc3ed46523"
        },
        {
          "id": "197E5C3C-D2F3-42D8-A536-875FB6D7D48C",
          "reportType": "PowerBIReport",
          "name": "NESGames",
          "datasetId": "7d6a4f72-1906-4e08-a469-bd6bc1ab7b69"
        }
      ]
    }
  ]
}
```

### Get workspaces with their 'users' expanded example.

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=users&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "e380d1d0-1fa6-460b-9a90-1a5c6b02414c",
      "isReadOnly": false,
      "isOnDedicatedCapacity": true,
      "capacityId": "0f084df7-c13d-451b-af5f-ed0c466403b2",
      "defaultDatasetStorageFormat": "Small",
      "name": "Sample Group 1",
      "description": "Sample group",
      "type": "Workspace",
      "state": "Active",
      "hasWorkspaceLevelSettings": false,
      "users": [
        {
          "emailAddress": "john@contoso.com",
          "groupUserAccessRight": "Admin"
        }
      ]
    },
    {
      "id": "183dcf10-47b8-48c4-84aa-f0bf9d5f8fcf",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "name": "Sample Group 2",
      "description": "Deleted sample group",
      "type": "Workspace",
      "state": "Deleted",
      "users": []
    }
  ]
}
```

### Get workspaces with their 'workbooks' expanded example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=workbooks&$top=100
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "94E57E92-CEE2-486D-8CC8-218C97200579",
      "isReadOnly": false,
      "isOnDedicatedCapacity": false,
      "description": "shorter description",
      "type": "Workspace",
      "state": "Removing",
      "hasWorkspaceLevelSettings": false,
      "name": "a",
      "workbooks": [
        {
          "name": "My Excel sheet",
          "datasetId": "8ce96c50-85a0-4db3-85c6-7ccc3ed46523"
        }
      ]
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| AdminDashboard | A Power BI dashboard returned by Admin APIs. The API returns a subset of the following list of dashboard properties. The subset depends on the API called, caller permissions, and the availability of data in the Power BI database. |
| AdminDataflow | The metadata of a dataflow returned by Admin APIs. Below is a list of properties that may be returned for a dataflow. Only a subset of the properties will be returned depending on the API called, the caller permissions and the availability of the data in the Power BI database. |
| AdminDataset | A Power BI dataset returned by Admin APIs. The API returns a subset of the following list of dataset properties. The subset depends on the API called, caller permissions, and the availability of the data in the Power BI database. |
| AdminGroup | A Power BI group returned by admin APIs |
| AdminGroups | The OData response wrapper for a list of Power BI groups returned by Admin APIs |
| AdminReport | A Power BI report returned by Admin APIs. The API returns a subset of the following list of report properties. The subset depends on the API called, caller permissions, and the availability of data in the Power BI database. |
| AdminTile | A Power BI tile returned by Admin APIs. |
| AzureResource | A response detailing a user-owned Azure resource such as a Log Analytics workspace. |
| DashboardUser | A Power BI user access right entry for a dashboard |
| DashboardUserAccessRight | The access right that the user has for the dashboard (permission level) |
| DataflowUser | A Power BI user access right entry for a dataflow |
| DataflowUserAccessRight | The access right that a user has for the dataflow (permission level) |
| DatasetQueryScaleOutSettings | Query scale-out settings of a dataset |
| DatasetUser | A Power BI user access right entry for a dataset |
| DatasetUserAccessRight | The access right that the user has for the dataset (permission level) |
| DefaultDatasetStorageFormat | The default dataset storage format in the group |
| DependentDataflow | A Power BI dependent dataflow |
| Encryption | Encryption information for a dataset |
| EncryptionStatus | Dataset encryption status |
| GroupType | The group type |
| GroupUser | A Power BI user with access to the workspace |
| GroupUserAccessRight | The access right (permission level) that a user has on the workspace |
| PrincipalType | The principal type |
| ReportUser | A Power BI user access right entry for a report |
| ReportUserAccessRight | The access right that the user has for the report (permission level) |
| ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| Subscription | An email subscription for a Power BI item (such as a report or a dashboard) |
| SubscriptionUser | A Power BI email subscription user |
| Workbook | A Power BI workbook |

### AdminDashboard

Object

A Power BI dashboard returned by Admin APIs. The API returns a subset of the following list of dashboard properties. The subset depends on the API called, caller permissions, and the availability of data in the Power BI database.

| Name | Type | Description |
| --- | --- | --- |
| appId | string | The app ID, returned only if the dashboard belongs to an app |
| displayName | string | The display name of the dashboard |
| embedUrl | string | The embed URL of the dashboard |
| id | string (uuid) | The dashboard ID |
| isReadOnly | boolean | Whether the dashboard is read-only |
| subscriptions | Subscription[] | (Empty Value) The subscription details for a Power BI item (such as a report or a dashboard). This property will be removed from the payload response in an upcoming release. You can retrieve subscription information for a Power BI report by using the [Get Report Subscriptions as Admin](/en-us/rest/api/power-bi/admin/reports-get-report-subscriptions-as-admin) API call. |
| tiles | AdminTile[] | The tiles that belong to the dashboard |
| users | DashboardUser[] | (Empty value) The dashboard user access details. This property will be removed from the payload response in an upcoming release. You can retrieve user information on a Power BI dashboard by using the [Get Dashboard Users as Admin](/en-us/rest/api/power-bi/admin/dashboards-get-dashboard-users-as-admin) API call, or the [PostWorkspaceInfo](/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info) API call with the `getArtifactUsers` parameter. |
| webUrl | string | The web URL of the dashboard |
| workspaceId | string (uuid) | The workspace ID (GUID) of the dashboard. This property will be returned only in GetDashboardsAsAdmin. |

### AdminDataflow

Object

The metadata of a dataflow returned by Admin APIs. Below is a list of properties that may be returned for a dataflow. Only a subset of the properties will be returned depending on the API called, the caller permissions and the availability of the data in the Power BI database.

| Name | Type | Description |
| --- | --- | --- |
| configuredBy | string | The dataflow owner |
| description | string | The dataflow description |
| modelUrl | string | A URL to the dataflow definition file (model.json) |
| name | string | The dataflow name |
| objectId | string (uuid) | The dataflow ID |
| users | DataflowUser[] | (Empty value) The dataflow user access details. This property will be removed from the payload response in an upcoming release. You can retrieve user information on a Power BI dataflow by using the [Get Dataflow Users as Admin](/en-us/rest/api/power-bi/admin/dataflows-get-dataflow-users-as-admin) API call, or the [PostWorkspaceInfo](/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info) API call with the `getArtifactUser` parameter. |
| workspaceId | string (uuid) | The dataflow workspace ID. |

### AdminDataset

Object

A Power BI dataset returned by Admin APIs. The API returns a subset of the following list of dataset properties. The subset depends on the API called, caller permissions, and the availability of the data in the Power BI database.

| Name | Type | Description |
| --- | --- | --- |
| ContentProviderType | string | The content provider type for the semantic model.<br><br>The following ContentProviderTypes are stored in the tenant home region:<br><br><br>| ContentProviderType |<br>| --- |<br>| Excel |<br>| CSV |<br>| UsageMetricsUserReport |<br>| UsageMetricsUserDashboard |<br>| RealTimeInPushMode |<br>| RealTimeInPubNubMode |<br>| RealTimeInStreamingMode |<br><br><br>The following ContentProviderTypes are stored in the Capacity region:<br><br><br>| ContentProviderType |<br>| --- |<br>| PowerBIDesktop |<br>| PowerBIModelingService |<br>| PbixInImportMode |<br>| PbixInDirectQueryMode |<br>| PbixInCompositeMode |<br>| InImportMode |<br>| InDirectQueryMode |<br>| InCompositeMode | |
| --- | --- | --- |
| Encryption | Encryption | Dataset encryption information. Only applicable when `$expand` is specified. |
| addRowsAPIEnabled | boolean | Whether the dataset allows adding new rows |
| configuredBy | string | The dataset owner |
| createReportEmbedURL | string | The dataset create report embed URL |
| createdDate | string (date-time) | The dataset creation date and time |
| description | string | The dataset description |
| id | string | The dataset ID |
| isEffectiveIdentityRequired | boolean | Whether the dataset requires an effective identity, which you must send in a [GenerateToken](/en-us/rest/api/power-bi/embed-token/generate-token) API call. |
| isEffectiveIdentityRolesRequired | boolean | Whether row-level security is defined inside the Power BI .pbix file. If so, you must specify a role. |
| isInPlaceSharingEnabled | boolean | Whether the dataset can be shared with external users to be consumed in their own tenant |
| isOnPremGatewayRequired | boolean | Whether the dataset requires an on-premises data gateway |
| isRefreshable | boolean | This field returns `true` when the dataset is either recently refreshed or is configured for automatic refresh, with the connection mode specifically set to 'Import'. The value will return `false` for other connection modes, such as 'DirectQuery' and 'LiveConnection', regardless of whether the dataset is manually refreshed or is set up for automatic refresh. |
| name | string | The dataset name |
| qnaEmbedURL | string | The dataset Q&A embed URL |
| queryScaleOutSettings | DatasetQueryScaleOutSettings | Query scale-out settings of a dataset |
| targetStorageMode | string | The dataset storage mode |
| upstreamDataflows | DependentDataflow[] | The list of all the dataflows this item depends on |
| users | DatasetUser[] | (Empty value) The dataset user access details. This property will be removed from the payload response in an upcoming release. You can retrieve user information on a Power BI item (such as a report or a dashboard) by using the [Get Dataset Users as Admin](/en-us/rest/api/power-bi/admin/datasets-get-dataset-users-as-admin) API, or the [PostWorkspaceInfo](/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info) API with the `getArtifactUsers` parameter. |
| webUrl | string | The web URL of the dataset |
| workspaceId | string (uuid) | The dataset workspace ID. This property will be returned only in GetDatasetsAsAdmin. |

### AdminGroup

Object

A Power BI group returned by admin APIs

| Name | Type | Description |
| --- | --- | --- |
| capacityId | string (uuid) | The capacity ID |
| dashboards | AdminDashboard[] | The dashboards that belong to the group |
| dataflowStorageId | string (uuid) | The Power BI dataflow storage account ID |
| dataflows | AdminDataflow[] | The dataflows that belong to the group |
| datasets | AdminDataset[] | The datasets that belong to the group |
| defaultDatasetStorageFormat | DefaultDatasetStorageFormat | The default dataset storage format in the workspace. Returned only when `isOnDedicatedCapacity` is `true` |
| description | string | The group description |
| hasWorkspaceLevelSettings | boolean | Whether the workspace has custom settings |
| id | string (uuid) | The workspace ID |
| isOnDedicatedCapacity | boolean | Whether the group is assigned to a dedicated capacity |
| isReadOnly | boolean | Whether the group is read-only |
| logAnalyticsWorkspace | AzureResource | The Log Analytics workspace assigned to the group. This is returned only when retrieving a single group. |
| name | string | The group name |
| pipelineId | string (uuid) | The deployment pipeline ID that the workspace is assigned to. |
| reports | AdminReport[] | The reports that belong to the group |
| state | string | The group state |
| type | GroupType | The type of group being returned. |
| users | GroupUser[] | (Empty value) The users that belong to the group and their access rights. This property will be removed from the payload response in an upcoming release. You can retrieve user information on a Power BI item (such as a report or a dashboard) by using the [Get Group Users As Admin](/en-us/rest/api/power-bi/admin/groups-get-group-users-as-admin) API call, or the [PostWorkspaceInfo](/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info) API call with the `getArtifactUsers` parameter. |
| workbooks | Workbook[] | The workbooks that belong to the group |

### AdminGroups

Object

The OData response wrapper for a list of Power BI groups returned by Admin APIs

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string | OData context |
| value | AdminGroup[] | The list of groups |

### AdminReport

Object

A Power BI report returned by Admin APIs. The API returns a subset of the following list of report properties. The subset depends on the API called, caller permissions, and the availability of data in the Power BI database.

| Name | Type | Description |
| --- | --- | --- |
| appId | string | The app ID, returned only if the report belongs to an app |
| createdBy | string | The report owner. Available only for reports created after June 2019. |
| createdDateTime | string (date-time) | The report creation date and time |
| datasetId | string | The dataset ID of the report |
| description | string | The report description |
| embedUrl | string | The embed URL of the report |
| format | string | The report definition format type. For **PowerBIReport**:<br><br>- [PBIR](/en-us/power-bi/developer/projects/projects-report?tabs=v2,desktop#pbir-format)<br>- [PBIR-Legacy](/en-us/power-bi/developer/projects/projects-report?tabs=v2,desktop#reportjson)<br><br><br>For **PaginatedReport**:<br><br>- [`RDL`](/en-us/power-bi/paginated-reports/report-definition-language) |
| id | string (uuid) | The report ID |
| isOwnedByMe | boolean | Indicates whether the current user has the ability to either modify or create a copy of the report. |
| modifiedBy | string | The last user that modified the report |
| modifiedDateTime | string (date-time) | The date and time that the report was last modified |
| name | string | The name of the report. App reports start with the prefix [App]. |
| originalReportObjectId | string (uuid) | The actual report ID when the workspace is published as an app. |
| reportType | enum:<br>- PaginatedReport<br>- PowerBIReport | The report type |
| subscriptions | Subscription[] | (Empty Value) The subscription details for a Power BI item (such as a report or a dashboard). This property will be removed from the payload response in an upcoming release. You can retrieve subscription information for a Power BI report by using the [Get Report Subscriptions as Admin](/en-us/rest/api/power-bi/admin/reports-get-report-subscriptions-as-admin) API call. |
| users | ReportUser[] | (Empty value) The user access details for a Power BI report. This property will be removed from the payload response in an upcoming release. You can retrieve user information on a Power BI report by using the [Get Report Users as Admin](/en-us/rest/api/power-bi/admin/reports-get-report-users-as-admin) API call, or the [PostWorkspaceInfo](/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info) API call with the `getArtifactUsers` parameter. |
| webUrl | string | The web URL of the report |
| workspaceId | string (uuid) | The workspace ID (GUID) of the report. This property will be returned only in GetReportsAsAdmin. |

### AdminTile

Object

A Power BI tile returned by Admin APIs.

| Name | Type | Description |
| --- | --- | --- |
| colSpan | integer | The number of tile span columns |
| datasetId | string | The dataset ID. Available only for tiles created from a report or by using a dataset, such as Q&A tiles. |
| embedData | string | The embed data for the tile |
| embedUrl | string | The embed URL of the tile |
| id | string (uuid) | The tile ID |
| reportId | string (uuid) | The report ID. Available only for tiles created from a report. |
| rowSpan | integer | The number of tile span rows |
| title | string | The display name of the tile |

### AzureResource

Object

A response detailing a user-owned Azure resource such as a Log Analytics workspace.

| Name | Type | Description |
| --- | --- | --- |
| id | string (uuid) | An identifier for the resource within Power BI. |
| resourceGroup | string | The resource group within the subscription where the resource resides. |
| resourceName | string | The name of the resource. |
| subscriptionId | string (uuid) | The Azure subscription where the resource resides. |

### DashboardUser

Object

A Power BI user access right entry for a dashboard

| Name | Type | Description |
| --- | --- | --- |
| dashboardUserAccessRight | DashboardUserAccessRight | The access right that the user has for the dashboard (permission level) |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| userType | string | Type of the user. |

### DashboardUserAccessRight

Enumeration

The access right that the user has for the dashboard (permission level)

| Value | Description |
| --- | --- |
| None | No permission to content in dashboard |
| Read | Grants Read access to content in dashboard |
| ReadWrite | Grants Read and Write access to content in dashboard |
| ReadReshare | Grants Read and Reshare access to content in dashboard |
| ReadCopy | Grants Read and Copy access to content in dashboard |
| Owner | Grants Read, Write and Reshare access to content in report |

### DataflowUser

Object

A Power BI user access right entry for a dataflow

| Name | Type | Description |
| --- | --- | --- |
| DataflowUserAccessRight | DataflowUserAccessRight | The access right that a user has for the dataflow (permission level) |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| userType | string | Type of the user. |

### DataflowUserAccessRight

Enumeration

The access right that a user has for the dataflow (permission level)

| Value | Description |
| --- | --- |
| None | Removes permission to content in dataflow |
| Read | Grants Read access to content in dataflow |
| ReadWrite | Grants Read and Write access to content in dataflow |
| ReadReshare | Grants Read and Reshare access to content in dataflow |
| Owner | Grants Read, Write and Reshare access to content in dataflow |

### DatasetQueryScaleOutSettings

Object

Query scale-out settings of a dataset

| Name | Type | Description |
| --- | --- | --- |
| autoSyncReadOnlyReplicas | boolean | Whether the dataset automatically syncs read-only replicas |
| maxReadOnlyReplicas | integer <br>minimum: -1maximum: 64 | Maximum number of read-only replicas for the dataset (0-64, -1 for automatic number of replicas) |

### DatasetUser

Object

A Power BI user access right entry for a dataset

| Name | Type | Description |
| --- | --- | --- |
| datasetUserAccessRight | DatasetUserAccessRight | The access right that the user has for the dataset (permission level) |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| userType | string | Type of the user. |

### DatasetUserAccessRight

Enumeration

The access right that the user has for the dataset (permission level)

| Value | Description |
| --- | --- |
| None | Removes permission to the content in the dataset |
| Read | Grants Read access to the content in the dataset |
| ReadWrite | Grants Read and Write access to the content in the dataset |
| ReadReshare | Grants Read and Reshare access to the content in the dataset |
| ReadWriteReshare | Grants Read, Write, and Reshare access to the content in the dataset |
| ReadExplore | Grants Read and Explore access to the content in the dataset |
| ReadReshareExplore | Grants Read, Reshare, and Explore access to the content in the dataset |
| ReadWriteExplore | Grants Read, Write, and Explore access to the content in the dataset |
| ReadWriteReshareExplore | Grants Read, Write, Reshare, and Explore access to the content in the dataset |

### DefaultDatasetStorageFormat

Enumeration

The default dataset storage format in the group

| Value | Description |
| --- | --- |
| Small | Small dataset storage format |
| Large | Large dataset storage format |

### DependentDataflow

Object

A Power BI dependent dataflow

| Name | Type | Description |
| --- | --- | --- |
| groupId | string | The target group ID |
| targetDataflowId | string | The target dataflow ID |

### Encryption

Object

Encryption information for a dataset

| Name | Type | Description |
| --- | --- | --- |
| EncryptionStatus | EncryptionStatus | Dataset encryption status |

### EncryptionStatus

Enumeration

Dataset encryption status

| Value | Description |
| --- | --- |
| Unknown | The encryption status is unknown due to dataset corruption |
| NotSupported | Encryption isn't supported for this dataset |
| InSyncWithWorkspace | Encryption is supported and is in sync with the encryption settings |
| NotInSyncWithWorkspace | Encryption is supported but isn't in sync with the encryption settings |

### GroupType

Enumeration

The group type

| Value | Description |
| --- | --- |
| AdminWorkspace | Admin Monitoring for Fabric Administrators |
| PersonalGroup | “My workspace”, also known as personal workspace |
| Personal | Special type of workspace meant for SharePoint list and OneDrive integration |
| Group | V1 version of shared workspace. This type of workspaces will be deprecated as Microsoft migrate all workspaces to latest version of shared workspace |
| Workspace | Shared workspace or simple workspace used to share content with other users in the organization |

### GroupUser

Object

A Power BI user with access to the workspace

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| groupUserAccessRight | GroupUserAccessRight | The access right (permission level) that a user has on the workspace |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| userType | string | Type of the user. |

### GroupUserAccessRight

Enumeration

The access right (permission level) that a user has on the workspace

| Value | Description |
| --- | --- |
| None | No access to workspace content |
| Member | Read, reshare and explore (ReadReshareExplore) access rights to workspace content |
| Admin | Administrator rights to workspace content |
| Contributor | Read and explore (ReadExplore) access to workspace content |
| Viewer | Read-only (Read) access to workspace content |

### PrincipalType

Enumeration

The principal type

| Value | Description |
| --- | --- |
| None | No principal type. Use for whole organization level access. |
| User | User principal type |
| Group | Group principal type |
| App | Service principal type |

### ReportUser

Object

A Power BI user access right entry for a report

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| reportUserAccessRight | ReportUserAccessRight | The access right that the user has for the report (permission level) |
| userType | string | Type of the user. |

### ReportUserAccessRight

Enumeration

The access right that the user has for the report (permission level)

| Value | Description |
| --- | --- |
| None | No permission to content in report |
| Read | Grants Read access to content in report |
| ReadWrite | Grants Read and Write access to content in report |
| ReadReshare | Grants Read and Reshare access to content in report |
| ReadCopy | Grants Read and Copy access to content in report |
| Owner | Grants Read, Write and Reshare access to content in report |

### ServicePrincipalProfile

Object

A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy).

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | The service principal profile name |
| id | string (uuid) | The service principal profile ID |

### Subscription

Object

An email subscription for a Power BI item (such as a report or a dashboard)

| Name | Type | Description |
| --- | --- | --- |
| artifactDisplayName | string | The name of the subscribed Power BI item (such as a report or a dashboard) |
| artifactId | string (uuid) | The ID of the subscribed Power BI item (such as a report or a dashboard) |
| artifactType | string | The type of Power BI item (for example a `Report`, `Dashboard`, or `Dataset`) |
| attachmentFormat | string | Format of the report attached in the email subscription |
| endDate | string (date-time) | The end date and time of the email subscription |
| frequency | string | The frequency of the email subscription |
| id | string (uuid) | The subscription ID |
| isEnabled | boolean | Whether the email subscription is enabled |
| linkToContent | boolean | Whether a subscription link exists in the email subscription |
| previewImage | boolean | Whether a screenshot of the report exists in the email subscription |
| startDate | string (date-time) | The start date and time of the email subscription |
| subArtifactDisplayName | string | The page name of the subscribed Power BI item, if it's a report. |
| title | string | The app name |
| users | SubscriptionUser[] | The details of each email subscriber. When using the [Get User Subscriptions As Admin](/en-us/rest/api/power-bi/admin/users-get-user-subscriptions-as-admin) API call, the returned value is an empty array (null). This property will be removed from the payload response in an upcoming release. You can retrieve subscription information on a Power BI report or dashboard by using the [Get Report Subscriptions As Admin](/en-us/rest/api/power-bi/admin/reports-get-report-subscriptions-as-admin) or [Get Dashboard Subscriptions As Admin](/en-us/rest/api/power-bi/admin/dashboards-get-dashboard-subscriptions-as-admin) API calls. |

### SubscriptionUser

Object

A Power BI email subscription user

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| userType | string | Type of the user. |

### Workbook

Object

A Power BI workbook

| Name | Type | Description |
| --- | --- | --- |
| datasetId | string | The ID of the dataset associated with a workbook. Only applies if the workbook has an associated dataset. |
| name | string | The workbook name |