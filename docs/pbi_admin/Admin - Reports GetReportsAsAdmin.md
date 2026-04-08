---
layout: Reference
title: Admin - Reports GetReportsAsAdmin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-reports-as-admin
uid: api.powerbi.com.power-bi.admin.reports_getreportsasadmin
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
description: Returns a list of reports for the organization. Permissions The user must be a Fabric administrator or authenticate using a service principal.
locale: en-us
document_id: 81a27fd6-349c-b9c2-44c1-3d71c7f887d3
document_version_independent_id: a72413ef-b505-e58a-136d-2821800233be
updated_at: 2025-12-11T12:31:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Reports-Get-Reports-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/5cbadd675c2ac29606a75191ea4880580fc78369/docs-ref-autogen/power-bi/Admin/Reports-Get-Reports-As-Admin.yml
git_commit_id: 5cbadd675c2ac29606a75191ea4880580fc78369
site_name: Docs
depot_name: MSDN.powerbi-rest-api
page_type: rest
page_kind: operation
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.powerbi-rest-api/{branchName}{pdfName}
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-bi/admin/reports-get-reports-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Reports-Get-Reports-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 4191233a-9254-ff61-dcbd-c7a9de6f1b86
---

# Admin - Reports GetReportsAsAdmin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of reports for the organization.

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
GET https://api.powerbi.com/v1.0/myorg/admin/reports
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/reports?$filter={$filter}&$top={$top}&$skip={$skip}
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
| 200 OK | AdminReports | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/reports
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
      "id": "5b218778-e7a5-4d73-8187-f10824047715",
      "name": "SalesMarketing",
      "webUrl": "https://app.powerbi.com//reports/5b218778-e7a5-4d73-8187-f10824047715",
      "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715",
      "workspaceId": "278e22a3-2aee-4057-886d-c3225423bc10"
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| AdminReport | A Power BI report returned by Admin APIs. The API returns a subset of the following list of report properties. The subset depends on the API called, caller permissions, and the availability of data in the Power BI database. |
| AdminReports | OData response wrapper for a Power BI Admin report collection |
| PrincipalType | The principal type |
| ReportUser | A Power BI user access right entry for a report |
| ReportUserAccessRight | The access right that the user has for the report (permission level) |
| ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| Subscription | An email subscription for a Power BI item (such as a report or a dashboard) |
| SubscriptionUser | A Power BI email subscription user |

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

### AdminReports

Object

OData response wrapper for a Power BI Admin report collection

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string | OData context |
| value | AdminReport[] | The report collection |

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