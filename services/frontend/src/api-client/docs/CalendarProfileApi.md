# CalendarProfileApi

All URIs are relative to _http://localhost_

| Method                                          | HTTP request                                            | Description           |
| ----------------------------------------------- | ------------------------------------------------------- | --------------------- |
| [**addProfileSource**](#addprofilesource)       | **POST** /api/profile/{profile_id}/source               | Add Profile Source    |
| [**createProfile**](#createprofile)             | **POST** /api/profile                                   | Create Profile        |
| [**deleteProfile**](#deleteprofile)             | **DELETE** /api/profile/{profile_id}                    | Delete Profile        |
| [**deleteProfileSource**](#deleteprofilesource) | **DELETE** /api/profile/{profile_id}/source/{source_id} | Delete Profile Source |
| [**getProfile**](#getprofile)                   | **GET** /api/profile/{profile_id}                       | Get Profile           |
| [**listProfileSources**](#listprofilesources)   | **GET** /api/profile/{profile_id}/source                | List Profile Sync     |
| [**listProfiles**](#listprofiles)               | **GET** /api/profile                                    | List Profiles         |
| [**triggerProfileSync**](#triggerprofilesync)   | **POST** /api/profile/{profile_id}/sync                 | Trigger Profile Sync  |
| [**updateProfile**](#updateprofile)             | **PUT** /api/profile/{profile_id}                       | Update Profile        |

# **addProfileSource**

> any addProfileSource(sourceCreate)

### Example

```typescript
import { CalendarProfileApi, Configuration, SourceCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let sourceCreate: SourceCreate; //

const { status, data } = await apiInstance.addProfileSource(
  profileId,
  sourceCreate
);
```

### Parameters

| Name             | Type             | Description | Notes                 |
| ---------------- | ---------------- | ----------- | --------------------- |
| **sourceCreate** | **SourceCreate** |             |                       |
| **profileId**    | [**string**]     |             | defaults to undefined |

### Return type

**any**

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

# **createProfile**

> ProfileReadShort createProfile(profileCreate)

### Example

```typescript
import { CalendarProfileApi, Configuration, ProfileCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileCreate: ProfileCreate; //

const { status, data } = await apiInstance.createProfile(profileCreate);
```

### Parameters

| Name              | Type              | Description | Notes |
| ----------------- | ----------------- | ----------- | ----- |
| **profileCreate** | **ProfileCreate** |             |       |

### Return type

**ProfileReadShort**

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

# **deleteProfile**

> deleteProfile()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)

const { status, data } = await apiInstance.deleteProfile(profileId);
```

### Parameters

| Name          | Type         | Description | Notes                 |
| ------------- | ------------ | ----------- | --------------------- |
| **profileId** | [**string**] |             | defaults to undefined |

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

# **deleteProfileSource**

> deleteProfileSource()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let sourceId: string; // (default to undefined)

const { status, data } = await apiInstance.deleteProfileSource(
  profileId,
  sourceId
);
```

### Parameters

| Name          | Type         | Description | Notes                 |
| ------------- | ------------ | ----------- | --------------------- |
| **profileId** | [**string**] |             | defaults to undefined |
| **sourceId**  | [**string**] |             | defaults to undefined |

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

# **getProfile**

> ProfileReadFull getProfile()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)

const { status, data } = await apiInstance.getProfile(profileId);
```

### Parameters

| Name          | Type         | Description | Notes                 |
| ------------- | ------------ | ----------- | --------------------- |
| **profileId** | [**string**] |             | defaults to undefined |

### Return type

**ProfileReadFull**

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

# **listProfileSources**

> Array<SourceRead> listProfileSources()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)

const { status, data } = await apiInstance.listProfileSources(profileId);
```

### Parameters

| Name          | Type         | Description | Notes                 |
| ------------- | ------------ | ----------- | --------------------- |
| **profileId** | [**string**] |             | defaults to undefined |

### Return type

**Array<SourceRead>**

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

# **listProfiles**

> Array<ProfileReadShort> listProfiles()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

const { status, data } = await apiInstance.listProfiles();
```

### Parameters

This endpoint does not have any parameters.

### Return type

**Array<ProfileReadShort>**

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

# **triggerProfileSync**

> any triggerProfileSync()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)

const { status, data } = await apiInstance.triggerProfileSync(profileId);
```

### Parameters

| Name          | Type         | Description | Notes                 |
| ------------- | ------------ | ----------- | --------------------- |
| **profileId** | [**string**] |             | defaults to undefined |

### Return type

**any**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **202**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateProfile**

> ProfileReadShort updateProfile(profileCreate)

### Example

```typescript
import { CalendarProfileApi, Configuration, ProfileCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let profileCreate: ProfileCreate; //

const { status, data } = await apiInstance.updateProfile(
  profileId,
  profileCreate
);
```

### Parameters

| Name              | Type              | Description | Notes                 |
| ----------------- | ----------------- | ----------- | --------------------- |
| **profileCreate** | **ProfileCreate** |             |                       |
| **profileId**     | [**string**]      |             | defaults to undefined |

### Return type

**ProfileReadShort**

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
