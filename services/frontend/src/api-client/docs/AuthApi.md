# AuthApi

All URIs are relative to _http://localhost_

| Method                    | HTTP request                | Description |
| ------------------------- | --------------------------- | ----------- |
| [**getToken**](#gettoken) | **GET** /api/auth/token     | Get Token   |
| [**login**](#login)       | **POST** /api/auth/login    | Login       |
| [**logout**](#logout)     | **POST** /api/auth/logout   | Logout      |
| [**me**](#me)             | **GET** /api/auth/me        | Me          |
| [**register**](#register) | **POST** /api/auth/register | Register    |

# **getToken**

> any getToken()

### Example

```typescript
import { AuthApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.getToken();
```

### Parameters

This endpoint does not have any parameters.

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
| **200**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login**

> TokenResponse login(loginRequest)

### Example

```typescript
import { AuthApi, Configuration, LoginRequest } from "./api";

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let loginRequest: LoginRequest; //

const { status, data } = await apiInstance.login(loginRequest);
```

### Parameters

| Name             | Type             | Description | Notes |
| ---------------- | ---------------- | ----------- | ----- |
| **loginRequest** | **LoginRequest** |             |       |

### Return type

**TokenResponse**

### Authorization

No authorization required

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

# **logout**

> any logout()

### Example

```typescript
import { AuthApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.logout();
```

### Parameters

This endpoint does not have any parameters.

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
| **200**     | Successful Response | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **me**

> any me()

### Example

```typescript
import { AuthApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.me();
```

### Parameters

This endpoint does not have any parameters.

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
| **200**     | Successful Response | -                |
| **401**     | Unauthorized        | -                |
| **403**     | Forbidden           | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register**

> TokenResponse register(registerRequest)

### Example

```typescript
import { AuthApi, Configuration, RegisterRequest } from "./api";

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let registerRequest: RegisterRequest; //

const { status, data } = await apiInstance.register(registerRequest);
```

### Parameters

| Name                | Type                | Description | Notes |
| ------------------- | ------------------- | ----------- | ----- |
| **registerRequest** | **RegisterRequest** |             |       |

### Return type

**TokenResponse**

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
