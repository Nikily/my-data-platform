---
layout: Reference
title: Admin - Datasets GetDatasetsAsAdmin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/datasets-get-datasets-as-admin
uid: api.powerbi.com.power-bi.admin.datasets_getdatasetsasadmin
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
description: Returns a list of datasets for the organization. Permissions The user must be a Fabric administrator or authenticate using a service principal.
locale: en-us
document_id: be096a14-1086-b514-7bc3-fa5f13b0873a
document_version_independent_id: 77ecfae3-152d-e347-828b-c6710f9ac650
updated_at: 2026-03-16T22:05:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Datasets-Get-Datasets-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/126d8a75bf5d035e45ba75d3656a5f82fcc0c9b5/docs-ref-autogen/power-bi/Admin/Datasets-Get-Datasets-As-Admin.yml
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
asset_id: api/power-bi/admin/datasets-get-datasets-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Datasets-Get-Datasets-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 53e2e12c-3933-c43c-dbfd-9aac948fb39e
---

# Admin - Datasets GetDatasetsAsAdmin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of datasets for the organization.

## Permissions

- The user must be a Fabric administrator or authenticate using a service principal.
- Delegated permissions are supported.

When running under service prinicipal authentication, an app **must not** have any admin-consent required premissions for Power BI set on it in the Azure portal.

## Required Scope

Tenant.Read.All or Tenant.ReadWrite.All

Relevant only when authenticating via a standard delegated admin access token. Must not be present when authentication via a service principal is used.

## Limitations

Maximum 50 requests per hour or 5 requests per minute, per tenant. 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/datasets
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/datasets?$filter={$filter}&$top={$top}&$skip={$skip}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| $filter | query |  | string | Returns a subset of a results based on [Odata](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptions) filter query parameter condition. |
| $skip | query |  | integer (int32) | Skips the first n results |
| $top | query |  | integer (int32) | Returns only the first n results |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdminDatasets | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/datasets
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
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
      "workspaceId": "5c968528-70b6-4588-809f-ce811ffa5c23"
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| AdminDataset | A Power BI dataset returned by Admin APIs. The API returns a subset of the following list of dataset properties. The subset depends on the API called, caller permissions, and the availability of the data in the Power BI database. |
| AdminDatasets | A dataset odata list wrapper |
| DatasetQueryScaleOutSettings | Query scale-out settings of a dataset |
| DatasetUser | A Power BI user access right entry for a dataset |
| DatasetUserAccessRight | The access right that the user has for the dataset (permission level) |
| DependentDataflow | A Power BI dependent dataflow |
| Encryption | Encryption information for a dataset |
| EncryptionStatus | Dataset encryption status |
| PrincipalType | The principal type |
| ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |

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

### AdminDatasets

Object

A dataset odata list wrapper

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string | OData context |
| value | AdminDataset[] | The datasets |

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

### PrincipalType

Enumeration

The principal type

| Value | Description |
| --- | --- |
| None | No principal type. Use for whole organization level access. |
| User | User principal type |
| Group | Group principal type |
| App | Service principal type |

### ServicePrincipalProfile

Object

A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy).

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | The service principal profile name |
| id | string (uuid) | The service principal profile ID |