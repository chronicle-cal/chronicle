# CalendarApi

All URIs are relative to _http://localhost_

| Method                                | HTTP request                           | Description     |
| ------------------------------------- | -------------------------------------- | --------------- |
| [**createCalendar**](#createcalendar) | **POST** /api/calendar                 | Create Calendar |
| [**deleteCalendar**](#deletecalendar) | **DELETE** /api/calendar/{calendar_id} | Delete Calendar |
| [**getCalendar**](#getcalendar)       | **GET** /api/calendar/{calendar_id}    | Get Calendar    |
| [**listCalendars**](#listcalendars)   | **GET** /api/calendar                  | List Calendars  |
| [**updateCalendar**](#updatecalendar) | **PUT** /api/calendar/{calendar_id}    | Update Calendar |

# **createCalendar**

> CalendarRead createCalendar(calendarCreate)

Create a new calendar for the current user.

### Example

```typescript
import { CalendarApi, Configuration, CalendarCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarCreate: CalendarCreate; //

const { status, data } = await apiInstance.createCalendar(calendarCreate);
```

### Parameters

| Name               | Type               | Description | Notes |
| ------------------ | ------------------ | ----------- | ----- |
| **calendarCreate** | **CalendarCreate** |             |       |

### Return type

**CalendarRead**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **201**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteCalendar**

> deleteCalendar()

Delete a calendar by ID.

### Example

```typescript
import { CalendarApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarId: string; // (default to undefined)

const { status, data } = await apiInstance.deleteCalendar(calendarId);
```

### Parameters

| Name           | Type         | Description | Notes                 |
| -------------- | ------------ | ----------- | --------------------- |
| **calendarId** | [**string**] |             | defaults to undefined |

### Return type

void (empty response body)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **204**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getCalendar**

> CalendarRead getCalendar()

Retrieve a calendar by ID.

### Example

```typescript
import { CalendarApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarId: string; // (default to undefined)

const { status, data } = await apiInstance.getCalendar(calendarId);
```

### Parameters

| Name           | Type         | Description | Notes                 |
| -------------- | ------------ | ----------- | --------------------- |
| **calendarId** | [**string**] |             | defaults to undefined |

### Return type

**CalendarRead**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listCalendars**

> Array<CalendarRead> listCalendars()

Retrieve all calendars for the current user.

### Example

```typescript
import { CalendarApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

const { status, data } = await apiInstance.listCalendars();
```

### Parameters

This endpoint does not have any parameters.

### Return type

**Array<CalendarRead>**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateCalendar**

> CalendarRead updateCalendar(calendarCreate)

Update a calendar by ID.

### Example

```typescript
import { CalendarApi, Configuration, CalendarCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarApi(configuration);

let calendarId: string; // (default to undefined)
let calendarCreate: CalendarCreate; //

const { status, data } = await apiInstance.updateCalendar(
  calendarId,
  calendarCreate
);
```

### Parameters

| Name               | Type               | Description | Notes                 |
| ------------------ | ------------------ | ----------- | --------------------- |
| **calendarCreate** | **CalendarCreate** |             |                       |
| **calendarId**     | [**string**]       |             | defaults to undefined |

### Return type

**CalendarRead**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
