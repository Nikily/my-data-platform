---
layout: Reference
title: Admin - WorkspaceInfo GetScanStatus - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-status
uid: api.powerbi.com.power-bi.admin.workspaceinfo_getscanstatus
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
description: Gets the scan status for the specified scan. Permissions The user must be a Fabric administrator or authenticate using a service principal.
locale: en-us
document_id: 748b4e5d-b21b-f779-5a86-a461840652e3
document_version_independent_id: 7db9f2f1-a1f9-7795-c3e2-7339bda4e050
updated_at: 2025-03-25T15:39:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Workspace-Info-Get-Scan-Status.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/4e3308b21f7552467b4f853dc62dbcc06b241147/docs-ref-autogen/power-bi/Admin/Workspace-Info-Get-Scan-Status.yml
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
asset_id: api/power-bi/admin/workspace-info-get-scan-status
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Workspace-Info-Get-Scan-Status.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 4a61098f-3f83-f471-3771-00468d5324c5
---

# Admin - WorkspaceInfo GetScanStatus

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Gets the scan status for the specified scan.

## Permissions

The user must be a Fabric administrator or authenticate using a service principal.

When running under service principal authentication, an app **must not** have any admin-consent required permissions for Power BI set on it in the Azure portal.

## Required Scope

Tenant.Read.All or Tenant.ReadWrite.All

Relevant only when authenticating via a standard delegated admin access token. Must not be present when authentication via a service principal is used.

## Limitations

Maximum 10,000 requests per hour. 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/{scanId}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| scanId | path | True | string (uuid) | The scan ID, which is included in the response from the workspaces or the [Admin - WorkspaceInfo PostWorkspaceInfo](/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info) API call that triggered the scan. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ScanRequest | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/e7d03602-4873-4760-b37e-1563ef5358e3
```

#### Sample response

- Status code:
    - 200

```json
{
  "id": "e7d03602-4873-4760-b37e-1563ef5358e3",
  "createdDateTime": "2020-06-15T16:46:28.0487687Z",
  "status": "Succeeded"
}
```

## Definitions

| Name | Description |
| --- | --- |
| PowerBIApiErrorResponseDetail | Detailed information about a Power BI error response |
| ScanRequest | A scan request |

### PowerBIApiErrorResponseDetail

Object

Detailed information about a Power BI error response

| Name | Type | Description |
| --- | --- | --- |
| code | string | The error code |
| message | string | The error message |
| target | string | The error target |

### ScanRequest

Object

A scan request

| Name | Type | Description |
| --- | --- | --- |
| createdDateTime | string (date-time) | The scan creation date and time |
| error | PowerBIApiErrorResponseDetail | The scan error (if any) |
| id | string (uuid) | The scan ID |
| status | string | The scan state |