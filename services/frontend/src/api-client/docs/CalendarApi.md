# CalendarApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**createCalendarApiCalendarPost**](#createcalendarapicalendarpost) | **POST** /api/calendar | Create Calendar|
|[**deleteCalendarApiCalendarCalendarIdDelete**](#deletecalendarapicalendarcalendariddelete) | **DELETE** /api/calendar/{calendar_id} | Delete Calendar|
|[**getCalendarApiCalendarCalendarIdGet**](#getcalendarapicalendarcalendaridget) | **GET** /api/calendar/{calendar_id} | Get Calendar|
|[**listCalendarsApiCalendarGet**](#listcalendarsapicalendarget) | **GET** /api/calendar | List Calendars|
|[**updateCalendarApiCalendarCalendarIdPut**](#updatecalendarapicalendarcalendaridput) | **PUT** /api/calendar/{calendar_id} | Update Calendar|

# **createCalendarApiCalendarPost**
> CalendarRead createCalendarApiCalendarPost(calendarCreate)

Create a new calendar for the current user.

### Example

```typescript
import {
    CalendarApi,
    Configuration,
    CalendarCreate
} from './api';

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarCreate: CalendarCreate; //
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.createCalendarApiCalendarPost(
    calendarCreate,
    authorization
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **calendarCreate** | **CalendarCreate**|  | |
| **authorization** | [**string**] |  | (optional) defaults to undefined|


### Return type

**CalendarRead**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteCalendarApiCalendarCalendarIdDelete**
> deleteCalendarApiCalendarCalendarIdDelete()

Delete a calendar by ID.

### Example

```typescript
import {
    CalendarApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.deleteCalendarApiCalendarCalendarIdDelete(
    calendarId,
    authorization
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **calendarId** | [**string**] |  | defaults to undefined|
| **authorization** | [**string**] |  | (optional) defaults to undefined|


### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getCalendarApiCalendarCalendarIdGet**
> CalendarRead getCalendarApiCalendarCalendarIdGet()

Retrieve a calendar by ID.

### Example

```typescript
import {
    CalendarApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.getCalendarApiCalendarCalendarIdGet(
    calendarId,
    authorization
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **calendarId** | [**string**] |  | defaults to undefined|
| **authorization** | [**string**] |  | (optional) defaults to undefined|


### Return type

**CalendarRead**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listCalendarsApiCalendarGet**
> Array<CalendarRead> listCalendarsApiCalendarGet()

Retrieve all calendars for the current user.

### Example

```typescript
import {
    CalendarApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.listCalendarsApiCalendarGet(
    authorization
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **authorization** | [**string**] |  | (optional) defaults to undefined|


### Return type

**Array<CalendarRead>**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateCalendarApiCalendarCalendarIdPut**
> CalendarRead updateCalendarApiCalendarCalendarIdPut(calendarCreate)

Update a calendar by ID.

### Example

```typescript
import {
    CalendarApi,
    Configuration,
    CalendarCreate
} from './api';

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarId: string; // (default to undefined)
let calendarCreate: CalendarCreate; //
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.updateCalendarApiCalendarCalendarIdPut(
    calendarId,
    calendarCreate,
    authorization
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **calendarCreate** | **CalendarCreate**|  | |
| **calendarId** | [**string**] |  | defaults to undefined|
| **authorization** | [**string**] |  | (optional) defaults to undefined|


### Return type

**CalendarRead**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

