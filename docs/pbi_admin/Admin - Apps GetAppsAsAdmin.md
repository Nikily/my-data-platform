---
layout: Reference
title: Admin - Apps GetAppsAsAdmin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/apps-get-apps-as-admin
uid: api.powerbi.com.power-bi.admin.apps_getappsasadmin
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
description: Returns a list of apps in the organization. The query parameter $top is required. Permissions The user must be a Fabric administrator or authenticate using a se
locale: en-us
document_id: 4be43e55-74ad-cfbc-93d7-2ad319adba95
document_version_independent_id: 9b8d6971-0e26-6ea2-8d3b-6696d5bdac15
updated_at: 2025-03-25T15:39:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Apps-Get-Apps-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/4e3308b21f7552467b4f853dc62dbcc06b241147/docs-ref-autogen/power-bi/Admin/Apps-Get-Apps-As-Admin.yml
git_commit_id: 4e3308b21f7552467b4f853dc62dbcc06b241147
site_name: Docs
depot_name: MSDN.powerbi-rest-api
page_type: rest
page_kind: operation
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.powerbi-rest-api/{branchName}{pdfName}
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-bi/admin/apps-get-apps-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Apps-Get-Apps-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: e000d5b6-82a1-f92a-5172-1840701f50db
---

# Admin - Apps GetAppsAsAdmin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of apps in the organization.

The query parameter $top is required.

## Permissions

- The user must be a Fabric administrator or authenticate using a service principal.
- Delegated permissions are supported.

When running under service prinicipal authentication, an app **must not** have any admin-consent required premissions for Power BI set on it in the Azure portal.

## Required Scope

Tenant.Read.All or Tenant.ReadWrite.All

Relevant only when authenticating via a standard delegated admin access token. Must not be present when authentication via a service principal is used.

## Limitations

Maximum 200 requests per hour. 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/apps?$top={$top}
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/apps?$top={$top}&$skip={$skip}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| $top | query | True | integer <br>minimum: 1 | The requested number of apps. |
| $skip | query |  | integer <br>minimum: 1 | The number entries to be skipped. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdminApps | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/apps?$top=10
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
      "description": "The finance app",
      "name": "Finance",
      "publishedBy": "Bill",
      "lastUpdate": "2019-01-13T09:46:53.094+02:00"
    },
    {
      "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
      "description": "The marketing app",
      "name": "Marketing",
      "publishedBy": "Ben",
      "lastUpdate": "2018-11-13T09:46:53.094+02:00"
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| AdminApp |  |
| AdminApps | The OData response wrapper for a list of Power BI installed apps for Admin APIs |

### AdminApp

Object

| Name | Type | Description |
| --- | --- | --- |
| description | string | The app description |
| id | string (uuid) | The app ID |
| lastUpdate | string (date-time) | The date and time the app was last updated |
| name | string | The app name |
| publishedBy | string | The app publisher |
| workspaceId | string | Associated workspace for the app |

### AdminApps

Object

The OData response wrapper for a list of Power BI installed apps for Admin APIs

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string | OData context |
| value | AdminApp[] | The list of installed apps |