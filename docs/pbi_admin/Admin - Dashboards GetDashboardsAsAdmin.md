---
layout: Reference
title: Admin - Dashboards GetDashboardsAsAdmin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-dashboards-as-admin
uid: api.powerbi.com.power-bi.admin.dashboards_getdashboardsasadmin
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
description: Returns a list of dashboards for the organization. Permissions The user must be a Fabric administrator or authenticate using a service principal.
locale: en-us
document_id: 615adc23-d06b-e305-1afe-23144e450b54
document_version_independent_id: bb6a9ce8-ba28-a531-8201-e435c6d591c4
updated_at: 2025-10-22T10:14:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Dashboards-Get-Dashboards-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/7f346ec2f925d5a3ca289a61020dcbebe3c41fd3/docs-ref-autogen/power-bi/Admin/Dashboards-Get-Dashboards-As-Admin.yml
git_commit_id: 7f346ec2f925d5a3ca289a61020dcbebe3c41fd3
site_name: Docs
depot_name: MSDN.powerbi-rest-api
page_type: rest
page_kind: operation
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.powerbi-rest-api/{branchName}{pdfName}
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-bi/admin/dashboards-get-dashboards-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Dashboards-Get-Dashboards-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 737fd583-838e-db16-bc73-718199eb124d
---

# Admin - Dashboards GetDashboardsAsAdmin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of dashboards for the organization.

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
GET https://api.powerbi.com/v1.0/myorg/admin/dashboards
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/dashboards?$expand={$expand}&$filter={$filter}&$top={$top}&$skip={$skip}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| $expand | query |  | string | Accepts a comma-separated list of data types, which will be expanded inline in the response. Supports `tiles`. |
| $filter | query |  | string | Returns a subset of a results based on [Odata](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptions) filter query parameter condition. |
| $skip | query |  | integer (int32) | Skips the first n results |
| $top | query |  | integer (int32) | Returns only the first n results |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdminDashboards | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/dashboards
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "displayName": "SalesMarketing",
      "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "isReadOnly": false,
      "workspaceId": "abfbdc89-2659-43c1-9142-93e8378eac96"
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| AdminDashboard | A Power BI dashboard returned by Admin APIs. The API returns a subset of the following list of dashboard properties. The subset depends on the API called, caller permissions, and the availability of data in the Power BI database. |
| AdminDashboards | The OData response wrapper for a Power BI dashboard collection |
| AdminTile | A Power BI tile returned by Admin APIs. |
| DashboardUser | A Power BI user access right entry for a dashboard |
| DashboardUserAccessRight | The access right that the user has for the dashboard (permission level) |
| PrincipalType | The principal type |
| ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| Subscription | An email subscription for a Power BI item (such as a report or a dashboard) |
| SubscriptionUser | A Power BI email subscription user |

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

### AdminDashboards

Object

The OData response wrapper for a Power BI dashboard collection

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string | OData context |
| value | AdminDashboard[] | The dashboard collection |

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