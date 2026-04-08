---
layout: Reference
title: Admin - Get Refreshables - REST API (Power BI Power BI REST APIs) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/get-refreshables
uid: api.powerbi.com.power-bi.admin.getrefreshables
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
description: Returns a list of refreshables for the organization within a capacity. Power BI retains a seven-day refresh history for each dataset, up to a maximum of sixty r
locale: en-us
document_id: a4244db0-fa18-96f8-8769-aef2b24877b1
document_version_independent_id: 1dc9eced-2576-ac36-169f-127210a5629f
updated_at: 2026-01-25T12:23:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/live/docs-ref-autogen/power-bi/Admin/Get-Refreshables.yml
gitcommit: https://github.com/MicrosoftDocs/powerbi-rest-api-docs-pr/blob/72b149723889c290f64069e141fdccbb9f2376aa/docs-ref-autogen/power-bi/Admin/Get-Refreshables.yml
git_commit_id: 72b149723889c290f64069e141fdccbb9f2376aa
site_name: Docs
depot_name: MSDN.powerbi-rest-api
page_type: rest
page_kind: operation
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.powerbi-rest-api/{branchName}{pdfName}
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-bi/admin/get-refreshables
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-bi/Admin/Get-Refreshables.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3197845-b4ce-44c6-a237-cd4be160e76c
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aea905fb-0a9d-4d46-b30f-e9cbaf772d1b
platformId: d17025d9-6bce-3126-0f81-879e78947724
---

# Admin - Get Refreshables

- Service:
    - Power BI REST APIs

- API Version:
    - v1.0

Returns a list of refreshables for the organization within a capacity.

Power BI retains a seven-day refresh history for each dataset, up to a maximum of sixty refreshes.

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
GET https://api.powerbi.com/v1.0/myorg/admin/capacities/refreshables?$top={$top}
```

 With optional parameters: 

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities/refreshables?$expand={$expand}&$filter={$filter}&$top={$top}&$skip={$skip}
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| $top | query | True | integer (int32)<br>minimum: 1 | Returns only the first n results. |
| $expand | query |  | string | Accepts a comma-separated list of data types, which will be expanded inline in the response. Supports `capacities` and `groups`. |
| $filter | query |  | string | Returns a subset of a results based on [Odata](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptions) filter query parameter condition. |
| $skip | query |  | integer (int32) | Skips the first n results. Use with top to fetch results beyond the first 1000. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | Refreshables | OK |

## Examples

| Example |
| --- |
| Get refreshables, filtering for an average refresh duration of greater than 30 minutes example. |
| Get refreshables with their 'capacity' and 'group' expanded example |

### Example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities/refreshables
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
      "kind": "Dataset",
      "startTime": "2017-06-13T09:25:43.153Z",
      "endTime": "2017-06-19T11:22:32.445Z",
      "refreshCount": 22,
      "refreshFailures": 0,
      "averageDuration": 289.3814,
      "medianDuration": 268.6245,
      "refreshesPerDay": 11,
      "lastRefresh": {
        "refreshType": "ViaApi",
        "startTime": "2017-06-13T09:25:43.153Z",
        "endTime": "2017-06-13T09:31:43.153Z",
        "status": "Completed",
        "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
      },
      "refreshSchedule": {
        "days": [
          "Sunday",
          "Friday",
          "Saturday"
        ],
        "times": [
          "05:00",
          "11:30",
          "17:30",
          "23:00"
        ],
        "enabled": true,
        "localTimeZoneId": "UTC",
        "notifyOption": "MailOnFailure"
      },
      "configuredBy": [
        "john@contoso.com"
      ]
    }
  ]
}
```

### Get refreshables, filtering for an average refresh duration of greater than 30 minutes example.

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities/refreshables?$filter=averageDuration gt 1800
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
      "kind": "Dataset",
      "startTime": "2017-06-13T09:25:43.153Z",
      "endTime": "2017-06-19T11:22:32.445Z",
      "refreshCount": 22,
      "refreshFailures": 0,
      "averageDuration": 3289.3814,
      "medianDuration": 2268.6245,
      "refreshesPerDay": 11,
      "lastRefresh": {
        "refreshType": "ViaApi",
        "startTime": "2017-06-13T09:25:43.153Z",
        "endTime": "2017-06-13T09:58:05.221Z",
        "status": "Completed",
        "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
      },
      "refreshSchedule": {
        "days": [
          "Sunday",
          "Friday",
          "Saturday"
        ],
        "times": [
          "05:00",
          "11:30",
          "17:30",
          "23:00"
        ],
        "enabled": true,
        "localTimeZoneId": "UTC",
        "notifyOption": "MailOnFailure"
      },
      "configuredBy": [
        "john@contoso.com"
      ]
    }
  ]
}
```

### Get refreshables with their 'capacity' and 'group' expanded example

#### Sample request

```http
GET https://api.powerbi.com/v1.0/myorg/admin/capacities/refreshables?$expand=capacity,group
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
      "kind": "Dataset",
      "startTime": "2017-06-13T09:25:43.153Z",
      "endTime": "2017-06-19T11:22:32.445Z",
      "refreshCount": 22,
      "refreshFailures": 0,
      "averageDuration": 289.3814,
      "medianDuration": 268.6245,
      "refreshesPerDay": 11,
      "lastRefresh": {
        "refreshType": "ViaApi",
        "startTime": "2017-06-13T09:25:43.153Z",
        "endTime": "2017-06-13T09:31:43.153Z",
        "status": "Completed",
        "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
      },
      "refreshSchedule": {
        "days": [
          "Sunday",
          "Friday",
          "Saturday"
        ],
        "times": [
          "05:00",
          "11:30",
          "17:30",
          "23:00"
        ],
        "enabled": true,
        "localTimeZoneId": "UTC",
        "notifyOption": "MailOnFailure"
      },
      "configuredBy": [
        "john@contoso.com"
      ],
      "capacity": {
        "id": "0f084df7-c13d-451b-af5f-ed0c466403b2",
        "displayName": "MyCapacity",
        "sku": "A1"
      },
      "group": {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing"
      }
    }
  ]
}
```

## Definitions

| Name | Description |
| --- | --- |
| Capacity | A Power BI capacity |
| CapacityState | The capacity state |
| capacityUserAccessRight | The access right that the user has on the capacity |
| days | The days on which to execute the refresh |
| Refresh | A Power BI refresh history entry |
| Refreshable | A Power BI refreshable is a dataset that's been refreshed at least once, or for which a valid refresh schedule exists. If a dataset doesn't meet either of these conditions, then it won't show up in the API response. Power BI retains a seven-day refresh history for each dataset, up to a maximum of sixty refreshes. |
| RefreshableGroup | A Power BI group associated to a Refreshable item |
| RefreshableKind | The refreshable kind |
| Refreshables | A Power BI refreshables list |
| RefreshAttempt | Power BI automatically makes multiple attempts to refresh a dataset if it experiences a refresh failure. This object contains information about each refresh attempt. |
| RefreshAttemptType | The type of refresh attempt. |
| RefreshSchedule | A Power BI refresh schedule for [imported model](/en-us/power-bi/connect-data/refresh-data#datasets-in-import-mode) |
| RefreshType | The type of refresh request |
| ScheduleNotifyOption | The notification option on termination of a scheduled refresh. Service principals only support the `NoNotification` value. |
| TenantKey | Encryption key information |

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

### days

Enumeration

The days on which to execute the refresh

| Value | Description |
| --- | --- |
| Monday |  |
| Tuesday |  |
| Wednesday |  |
| Thursday |  |
| Friday |  |
| Saturday |  |
| Sunday |  |

### Refresh

Object

A Power BI refresh history entry

| Name | Type | Description |
| --- | --- | --- |
| endTime | string (date-time) | The end date and time of the refresh (may be empty if a refresh is in progress) in UTC format. |
| refreshAttempts | RefreshAttempt[] | The refresh attempt list. |
| refreshType | RefreshType | The type of refresh request |
| requestId | string | The identifier of the refresh request. Provide this identifier in all service requests. |
| serviceExceptionJson | string | Failure error code in JSON format (empty if no error) |
| startTime | string (date-time) | The start date and time of the refresh in UTC format. |
| status | string | - `Unknown` if the completion state is unknown or a refresh is in progress.<br>- `Completed` for a successfully completed refresh.<br>- `Failed` for an unsuccessful refresh (`serviceExceptionJson` will contain the error code).<br>- `Disabled` if the refresh is disabled by a selective refresh. |

### Refreshable

Object

A Power BI refreshable is a dataset that's been refreshed at least once, or for which a valid refresh schedule exists. If a dataset doesn't meet either of these conditions, then it won't show up in the API response. Power BI retains a seven-day refresh history for each dataset, up to a maximum of sixty refreshes.

| Name | Type | Description |
| --- | --- | --- |
| averageDuration | number | The average duration in seconds of a refresh during the time window for which refresh data exists |
| capacity | Capacity | The capacity for the refreshable item |
| configuredBy | string[] | The refreshable owners |
| endTime | string (date-time) | The end time of the window for which refresh data exists in UTC format. |
| group | RefreshableGroup | The associated group for the refreshable item |
| id | string | The object ID of the refreshable |
| kind | RefreshableKind | The refreshable kind |
| lastRefresh | Refresh | The last Power BI refresh history entry for the refreshable item |
| medianDuration | number | The median duration in seconds of a refresh within the time window for which refresh data exists |
| name | string | The display name of the refreshable |
| refreshCount | integer | The number of refreshes within the time window for which refresh data exists |
| refreshFailures | integer | The number of refresh failures within the time window for which refresh data exists |
| refreshSchedule | RefreshSchedule | The refresh schedule for the refreshable item |
| refreshesPerDay | integer | The number of refreshes per day (scheduled and on-demand) within the time window for which refresh data exists |
| startTime | string (date-time) | The start time of the window for which refresh data exists in UTC format. |

### RefreshableGroup

Object

A Power BI group associated to a Refreshable item

| Name | Type | Description |
| --- | --- | --- |
| id | string (uuid) | The workspace ID |
| name | string | The group name |

### RefreshableKind

Enumeration

The refreshable kind

| Value | Description |
| --- | --- |
| Dataset | Dataset |

### Refreshables

Object

A Power BI refreshables list

| Name | Type | Description |
| --- | --- | --- |
| @odata.context | string | OData context |
| value | Refreshable[] | The refreshables |

### RefreshAttempt

Object

Power BI automatically makes multiple attempts to refresh a dataset if it experiences a refresh failure. This object contains information about each refresh attempt.

| Name | Type | Description |
| --- | --- | --- |
| attemptId | integer | The index of the refresh attempt. |
| endTime | string (date-time) | The end date and time of the refresh attempt. The value is void if the refresh attempt is in progress. |
| executionMetrics | object[] | The Analysis Services engine execution metrics captured during the refresh attempt. |
| serviceExceptionJson | string | Failure error code in JSON format. Void if there's no error. |
| startTime | string (date-time) | The start date and time of the refresh attempt. |
| type | RefreshAttemptType | The type of refresh attempt. |

### RefreshAttemptType

Enumeration

The type of refresh attempt.

| Value | Description |
| --- | --- |
| Data | The refresh attempt to load data into the dataset. |
| Query | The attempt to refresh premium query caches and dashboard tiles.u |

### RefreshSchedule

Object

A Power BI refresh schedule for [imported model](/en-us/power-bi/connect-data/refresh-data#datasets-in-import-mode)

| Name | Type | Description |
| --- | --- | --- |
| days | days[] | The days on which to execute the refresh |
| enabled | boolean | Whether the refresh is enabled |
| localTimeZoneId | string | The ID of the time zone to use. For more information, see [Time zone info](/en-us/dotnet/api/system.timezoneinfo.id). |
| notifyOption | ScheduleNotifyOption | The notification option on termination of a scheduled refresh. Service principals only support the `NoNotification` value. |
| times | string[] | The times of day to execute the refresh |

### RefreshType

Enumeration

The type of refresh request

| Value | Description |
| --- | --- |
| Scheduled | The refresh was triggered by a dataset refresh schedule setting |
| OnDemand | The refresh was triggered interactively through the Power BI portal |
| ViaApi | The refresh was triggered by an API call |
| ViaXmlaEndpoint | The refresh was triggered through Power BI public XMLA endpoint |
| ViaEnhancedApi | The refresh was triggered by an enhanced refresh REST API call |
| OnDemandTraining | The refresh was triggered interactively through the Power BI portal with automatic aggregations training |

### ScheduleNotifyOption

Enumeration

The notification option on termination of a scheduled refresh. Service principals only support the `NoNotification` value.

| Value | Description |
| --- | --- |
| NoNotification | No notification will be sent |
| MailOnFailure | A mail notification will be sent on refresh failure |

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