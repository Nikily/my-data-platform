---
layout: Reference
title: Admin - WidelySharedArtifacts LinksSharedToWholeOrganization - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/widely-shared-artifacts-links-shared-to-whole-organization
uid: api.powerbi.com.power-bi.admin.widelysharedartifacts_linkssharedtowholeorganization
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
description: Returns a list of Power BI reports that are shared with the whole organization through links. Permissions The user must be a Fabric administrator or authenticat
locale: en-us
document_id: 370bdfd7-3895-c917-0216-084483a84f16
document_version_independent_id: 1b6c0151-fa9e-3b56-75d1-65de9bfe5c14
updated_at: 2025-03-25T15:39:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Widely-Shared-Artifacts-Links-Shared-To-Whole-Organization.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/4e3308b21f7552467b4f853dc62dbcc06b241147/docs-ref-autogen/power-bi/Admin/Widely-Shared-Artifacts-Links-Shared-To-Whole-Organization.yml
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
asset_id: api/power-bi/admin/widely-shared-artifacts-links-shared-to-whole-organization
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Widely-Shared-Artifacts-Links-Shared-To-Whole-Organization.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: a842a8a0-225f-ad8c-09b5-4f04d38b0628
---

# Admin - WidelySharedArtifacts LinksSharedToWholeOrganization

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of Power BI reports that are shared with the whole organization through links.

## Permissions

- The user must be a Fabric administrator or authenticate using a service principal.
- Delegated permissions are supported.

## Required Scope

Tenant.Read.All or Tenant.ReadWrite.All

## Limitations

Maximum 200 requests per hour. 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/widelySharedArtifacts/linksSharedToWholeOrganization
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/widelySharedArtifacts/linksSharedToWholeOrganization?continuationToken={continuationToken}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| continuationToken | query |  | string | Token required to get the next chunk of the result set |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ArtifactAccessResponse | OK |

## Examples

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/widelySharedArtifacts/linksSharedToWholeOrganization
```

#### Sample response

- Status code:
    - 200

```json
{
  "artifactAccessEntities": [
    {
      "artifactId": "41ce06d1-d81b-4ea0-bc6d-2ce3dd2f8e87",
      "displayName": "test report",
      "artifactType": "Report",
      "accessRight": "ReadWrite",
      "shareType": "Link",
      "sharer": {
        "displayName": "John Nick",
        "emailAddress": "john@contoso.com",
        "identifier": "john@contoso.com",
        "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
        "principalType": "User"
      }
    }
  ],
  "continuationUri": "https://api.powerbi.com/v1.0/myorg/admin/widelySharedArtifacts/linksSharedToWholeOrganization?continuationToken='LDEsMTAwMDAwLDA%3D'",
  "continuationToken": "LDEsMTAwMDAwLDA%3D"
}
```

## Definitions

| Name | Description |
| --- | --- |
| ArtifactAccessEntry | A user access entry for a Power BI item |
| ArtifactAccessResponse | The OData response wrapper for a list of Power BI items (such as reports or dashboards) that a user can access |
| ArtifactType | The artifact type |
| PrincipalType | The principal type |
| ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| User | A Power BI user |

### ArtifactAccessEntry

Object

A user access entry for a Power BI item

| Name | Type | Description |
| --- | --- | --- |
| accessRight | string | The access right that the user has for the Power BI item |
| artifactId | string | The Power BI item ID |
| artifactType | ArtifactType | The type of Power BI item |
| displayName | string | The display name of the Power BI item |
| shareType | string | The type of how the access is given to the Power BI item. Only available for widely shared artifacts APIs. |
| sharer | User | The user who shared the Power BI item. Only available for widely shared artifacts APIs. |

### ArtifactAccessResponse

Object

The OData response wrapper for a list of Power BI items (such as reports or dashboards) that a user can access

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string |  |
| artifactAccessEntities | ArtifactAccessEntry[] | The list of Power BI items that a user can access |
| continuationToken | string | The token for the next chunk in the result set |
| continuationUri | string | The URI of the next chunk in the result set |

### ArtifactType

Enumeration

The artifact type

| Value | Description |
| --- | --- |
| Report | Power BI Report |
| PaginatedReport | Power BI Paginated Report |
| Dashboard | Power BI Dashboard |
| Dataset | Power BI Dataset |
| Dataflow | Power BI Dataflow |
| PersonalGroup | My workspace object |
| Group | V1 shared workspace object |
| Workspace | Shared workspace object |
| Capacity | Capacity object |
| App | Power BI Apps |

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

### User

Object

A Power BI user

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | Display name of the principal |
| emailAddress | string | Email address of the user |
| graphId | string | Identifier of the principal in Microsoft Graph. Only available for admin APIs. |
| identifier | string | Identifier of the principal |
| principalType | PrincipalType | The principal type |
| profile | ServicePrincipalProfile | A Power BI service principal profile. Only relevant for [Power BI Embedded multi-tenancy solution](/en-us/power-bi/developer/embedded/embed-multi-tenancy). |
| userType | string | Type of the user. |