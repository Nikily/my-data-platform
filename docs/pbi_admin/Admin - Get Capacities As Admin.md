---
layout: Reference
title: Admin - Get Capacities As Admin - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/get-capacities-as-admin
uid: api.powerbi.com.power-bi.admin.getcapacitiesasadmin
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
description: Returns a list of capacities for the organization. Permissions The user must be a Fabric administrator or authenticate using a service principal.
locale: en-us
document_id: d7062066-cd3f-7152-bfef-23bc110054d9
document_version_independent_id: 98064612-953c-2c48-8541-064b8404286d
updated_at: 2025-03-25T15:39:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Get-Capacities-As-Admin.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/4e3308b21f7552467b4f853dc62dbcc06b241147/docs-ref-autogen/power-bi/Admin/Get-Capacities-As-Admin.yml
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
asset_id: api/power-bi/admin/get-capacities-as-admin
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Get-Capacities-As-Admin.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: 497ebacb-aea5-1a37-8667-d2db48558479
---

# Admin - Get Capacities As Admin

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of capacities for the organization.

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
GET https://api.powerbi.com/v1.0/myorg/admin/capacities
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities?$expand={$expand}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| $expand | query |  | string | Expands related entities inline |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | Capacities | OK |

## Examples

| Example |
| --- |
| Example with expand on tenant key |

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "0f084df7-c13d-451b-af5f-ed0c466403b2",
      "displayName": "MyCapacity",
      "admins": [
        "john@contoso.com"
      ],
      "sku": "A1",
      "state": "Active",
      "region": "West Central US",
      "capacityUserAccessRight": "Admin",
      "tenantKeyId": "82d9a37a-2b45-4221-b012-cb109b8e30c7"
    }
  ]
}
```

### Example with expand on tenant key

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities?$expand=tenantKey
```

#### Sample response

- Status code:
    - 200

```json
{
  "value": [
    {
      "id": "0f084df7-c13d-451b-af5f-ed0c466403b2",
      "displayName": "MyCapacity",
      "admins": [
        "john@contoso.com"
      ],
      "sku": "A1",
      "state": "Active",
      "region": "West Central US",
      "capacityUserAccessRight": "Admin",
      "tenantKeyId": "82d9a37a-2b45-4221-b012-cb109b8e30c7",
      "tenantKey": {
        "id": "82d9a37a-2b45-4221-b012-cb109b8e30c7",
        "name": "Contoso Sales",
        "keyVaultKeyIdentifier": "https://contoso-vault2.vault.azure.net/keys/ContosoKeyVault/b2ab4ba1c7b341eea5ecaaa2wb54c4d2",
        "isDefault": true,
        "createdAt": "2019-04-30T21:35:15.867-07:00",
        "updatedAt": "2019-04-30T21:35:15.867-07:00"
      }
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| Capacities | OData response wrapper for a Power BI capacity list |
| Capacity | A Power BI capacity |
| CapacityState | The capacity state |
| capacityUserAccessRight | The access right that the user has on the capacity |
| TenantKey | Encryption key information |

### Capacities

Object

OData response wrapper for a Power BI capacity list

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string |  |
| value | Capacity[] | The capacity list |

### Capacity

Object

A Power BI capacity

| Name | Type | Description |
| --- | --- | --- |
| admins | string[] | An array of capacity admins |
| capacityUserAccessRight | capacityUserAccessRight | The access right a user has on the capacity |
| displayName | string | The display name of the capacity |
| id | string (uuid) | The capacity ID |
| region | string | The Azure region where the capacity was provisioned |
| sku | string | The capacity SKU |
| state | CapacityState | The capacity state |
| tenantKey | TenantKey | Encryption key information (only applies to admin routes) |
| tenantKeyId | string (uuid) | The ID of an encryption key (only applicable to the admin route) |

### CapacityState

Enumeration

The capacity state

| Value | Description |
| --- | --- |
| NotActivated | Unsupported |
| Active | The capacity is ready to use |
| Provisioning | Activation of the capacity is in progress |
| ProvisionFailed | Provisioning of the capacity failed |
| PreSuspended | Unsupported |
| Suspended | Use of the capacity is suspended |
| Deleting | Deletion of the capacity is in progress |
| Deleted | The capacity was deleted and is unavailable |
| Invalid | The capacity can't be used |
| UpdatingSku | A capacity SKU change is in progress |

### capacityUserAccessRight

Enumeration

The access right that the user has on the capacity

| Value | Description |
| --- | --- |
| None | User doesn't have access to the capacity |
| Assign | User has contributor rights and can assign workspaces to the capacity |
| Admin | User has administrator rights on the capacity |

### TenantKey

Object

Encryption key information

| Name | Type | Description |
| --- | --- | --- |
| createdAt | string (date-time) | The creation date and time of the encryption key |
| id | string (uuid) | The ID of the encryption key |
| isDefault | boolean | Whether the encryption key is the default key for the entire tenant. Any newly created capacity inherits the default key. |
| keyVaultKeyIdentifier | string | The URI that uniquely specifies the encryption key in Azure Key Vault |
| name | string | The name of the encryption key |
| updatedAt | string (date-time) | The last update date and time of the encryption key |