# CalendarProfileApi

All URIs are relative to _http://localhost_

| Method                                                                                                                        | HTTP request                                            | Description           |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------- |
| [**addProfileSourceApiProfileProfileIdSourcePost**](#addprofilesourceapiprofileprofileidsourcepost)                           | **POST** /api/profile/{profile_id}/source               | Add Profile Source    |
| [**createProfileApiProfilePost**](#createprofileapiprofilepost)                                                               | **POST** /api/profile                                   | Create Profile        |
| [**deleteProfileApiProfileProfileIdDelete**](#deleteprofileapiprofileprofileiddelete)                                         | **DELETE** /api/profile/{profile_id}                    | Delete Profile        |
| [**deleteProfileSourceApiProfileProfileIdSourceSourceIdDelete**](#deleteprofilesourceapiprofileprofileidsourcesourceiddelete) | **DELETE** /api/profile/{profile_id}/source/{source_id} | Delete Profile Source |
| [**getProfileApiProfileProfileIdGet**](#getprofileapiprofileprofileidget)                                                     | **GET** /api/profile/{profile_id}                       | Get Profile           |
| [**listProfileSyncApiProfileProfileIdSourceGet**](#listprofilesyncapiprofileprofileidsourceget)                               | **GET** /api/profile/{profile_id}/source                | List Profile Sync     |
| [**listProfilesApiProfileGet**](#listprofilesapiprofileget)                                                                   | **GET** /api/profile                                    | List Profiles         |
| [**triggerProfileSyncApiProfileProfileIdSyncPost**](#triggerprofilesyncapiprofileprofileidsyncpost)                           | **POST** /api/profile/{profile_id}/sync                 | Trigger Profile Sync  |
| [**updateProfileApiProfileProfileIdPut**](#updateprofileapiprofileprofileidput)                                               | **PUT** /api/profile/{profile_id}                       | Update Profile        |

# **addProfileSourceApiProfileProfileIdSourcePost**

> any addProfileSourceApiProfileProfileIdSourcePost(sourceCreate)

### Example

```typescript
import { CalendarProfileApi, Configuration, SourceCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let sourceCreate: SourceCreate; //
let authorization: string; // (optional) (default to undefined)

const { status, data } =
  await apiInstance.addProfileSourceApiProfileProfileIdSourcePost(
    profileId,
    sourceCreate,
    authorization
  );
```

### Parameters

| Name              | Type             | Description | Notes                            |
| ----------------- | ---------------- | ----------- | -------------------------------- |
| **sourceCreate**  | **SourceCreate** |             |                                  |
| **profileId**     | [**string**]     |             | defaults to undefined            |
| **authorization** | [**string**]     |             | (optional) defaults to undefined |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **201**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createProfileApiProfilePost**

> ProfileReadShort createProfileApiProfilePost(profileCreate)

### Example

```typescript
import { CalendarProfileApi, Configuration, ProfileCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileCreate: ProfileCreate; //
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.createProfileApiProfilePost(
  profileCreate,
  authorization
);
```

### Parameters

| Name              | Type              | Description | Notes                            |
| ----------------- | ----------------- | ----------- | -------------------------------- |
| **profileCreate** | **ProfileCreate** |             |                                  |
| **authorization** | [**string**]      |             | (optional) defaults to undefined |

### Return type

**ProfileReadShort**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **201**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteProfileApiProfileProfileIdDelete**

> deleteProfileApiProfileProfileIdDelete()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } =
  await apiInstance.deleteProfileApiProfileProfileIdDelete(
    profileId,
    authorization
  );
```

### Parameters

| Name              | Type         | Description | Notes                            |
| ----------------- | ------------ | ----------- | -------------------------------- |
| **profileId**     | [**string**] |             | defaults to undefined            |
| **authorization** | [**string**] |             | (optional) defaults to undefined |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **204**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteProfileSourceApiProfileProfileIdSourceSourceIdDelete**

> deleteProfileSourceApiProfileProfileIdSourceSourceIdDelete()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let sourceId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } =
  await apiInstance.deleteProfileSourceApiProfileProfileIdSourceSourceIdDelete(
    profileId,
    sourceId,
    authorization
  );
```

### Parameters

| Name              | Type         | Description | Notes                            |
| ----------------- | ------------ | ----------- | -------------------------------- |
| **profileId**     | [**string**] |             | defaults to undefined            |
| **sourceId**      | [**string**] |             | defaults to undefined            |
| **authorization** | [**string**] |             | (optional) defaults to undefined |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **204**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProfileApiProfileProfileIdGet**

> ProfileReadFull getProfileApiProfileProfileIdGet()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.getProfileApiProfileProfileIdGet(
  profileId,
  authorization
);
```

### Parameters

| Name              | Type         | Description | Notes                            |
| ----------------- | ------------ | ----------- | -------------------------------- |
| **profileId**     | [**string**] |             | defaults to undefined            |
| **authorization** | [**string**] |             | (optional) defaults to undefined |

### Return type

**ProfileReadFull**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listProfileSyncApiProfileProfileIdSourceGet**

> Array<SourceRead> listProfileSyncApiProfileProfileIdSourceGet()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } =
  await apiInstance.listProfileSyncApiProfileProfileIdSourceGet(
    profileId,
    authorization
  );
```

### Parameters

| Name              | Type         | Description | Notes                            |
| ----------------- | ------------ | ----------- | -------------------------------- |
| **profileId**     | [**string**] |             | defaults to undefined            |
| **authorization** | [**string**] |             | (optional) defaults to undefined |

### Return type

**Array<SourceRead>**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listProfilesApiProfileGet**

> Array<ProfileReadShort> listProfilesApiProfileGet()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let authorization: string; // (optional) (default to undefined)

const { status, data } =
  await apiInstance.listProfilesApiProfileGet(authorization);
```

### Parameters

| Name              | Type         | Description | Notes                            |
| ----------------- | ------------ | ----------- | -------------------------------- |
| **authorization** | [**string**] |             | (optional) defaults to undefined |

### Return type

**Array<ProfileReadShort>**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **triggerProfileSyncApiProfileProfileIdSyncPost**

> any triggerProfileSyncApiProfileProfileIdSyncPost()

### Example

```typescript
import { CalendarProfileApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let authorization: string; // (optional) (default to undefined)

const { status, data } =
  await apiInstance.triggerProfileSyncApiProfileProfileIdSyncPost(
    profileId,
    authorization
  );
```

### Parameters

| Name              | Type         | Description | Notes                            |
| ----------------- | ------------ | ----------- | -------------------------------- |
| **profileId**     | [**string**] |             | defaults to undefined            |
| **authorization** | [**string**] |             | (optional) defaults to undefined |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **202**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateProfileApiProfileProfileIdPut**

> ProfileReadShort updateProfileApiProfileProfileIdPut(profileCreate)

### Example

```typescript
import { CalendarProfileApi, Configuration, ProfileCreate } from "./api";

const configuration = new Configuration();
const apiInstance = new CalendarProfileApi(configuration);

let profileId: string; // (default to undefined)
let profileCreate: ProfileCreate; //
let authorization: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.updateProfileApiProfileProfileIdPut(
  profileId,
  profileCreate,
  authorization
);
```

### Parameters

| Name              | Type              | Description | Notes                            |
| ----------------- | ----------------- | ----------- | -------------------------------- |
| **profileCreate** | **ProfileCreate** |             |                                  |
| **profileId**     | [**string**]      |             | defaults to undefined            |
| **authorization** | [**string**]      |             | (optional) defaults to undefined |

### Return type

**ProfileReadShort**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
