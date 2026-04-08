---
layout: Reference
title: Admin - Groups GetUnusedArtifactsAsAdmin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/groups-get-unused-artifacts-as-admin
uid: api.powerbi.com.power-bi.admin.groups_getunusedartifactsasadmin
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
description: Returns a list of datasets, reports, and dashboards that have not been used within 30 days for the specified workspace.
locale: en-us
document_id: 94e7d301-058b-2097-335e-fa279b5ed654
document_version_independent_id: 9e74136e-7611-5918-cc19-ccb446fc8164
updated_at: 2025-03-25T15:39:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Groups-Get-Unused-Artifacts-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/4e3308b21f7552467b4f853dc62dbcc06b241147/docs-ref-autogen/power-bi/Admin/Groups-Get-Unused-Artifacts-As-Admin.yml
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
asset_id: api/power-bi/admin/groups-get-unused-artifacts-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Groups-Get-Unused-Artifacts-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 918a39a3-97b0-8ff0-bc1d-60a28799b7a3
---

# Admin - Groups GetUnusedArtifactsAsAdmin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of datasets, reports, and dashboards that have not been used within 30 days for the specified workspace. This is a preview API call.

## Permissions

- The user must be a Fabric administrator or authenticate using a service principal.
- Delegated permissions are supported.

## Required Scope

Tenant.Read.All or Tenant.ReadWrite.All

## Limitations

Maximum 200 requests per hour. 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups/{groupId}/unused
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups/{groupId}/unused?continuationToken={continuationToken}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| groupId | path | True | string (uuid) | The workspace ID |
| continuationToken | query |  | string | Token required to get the next chunk of the result set |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | UnusedArtifactsResponse | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/unused
```

#### Sample response

- Status code:
    - 200

## Definitions

| Name | Description |
| --- | --- |
| UnusedArtifactEntity | The unused Power BI item entity |
| UnusedArtifactsResponse | OData response wrapper for unused Power BI item (such as a report or a dashboard) entities |

### UnusedArtifactEntity

Object

The unused Power BI item entity

| Name | Type | Description |
| --- | --- | --- |
| artifactId | string | The ID of the Power BI item |
| artifactSizeInMB | integer | The size of the Power BI item in megabytes (if applicable) |
| artifactType | string | The Power BI item type |
| createdDateTime | string (date-time) | The creation time of the Power BI item (if applicable) |
| displayName | string | The display name of the Power BI item |
| lastAccessedDateTime | string (date-time) | The last access time of the Power BI item (if applicable) |

### UnusedArtifactsResponse

Object

OData response wrapper for unused Power BI item (such as a report or a dashboard) entities

| Name | Type | Description |
| --- | --- | --- |
| continuationToken | string | Token to get the next chunk of the result set |
| continuationUri | string | The URI for the next chunk in the result set |
| unusedArtifactEntities | UnusedArtifactEntity[] | The unused Power BI item entities |