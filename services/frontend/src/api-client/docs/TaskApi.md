# TaskApi

All URIs are relative to _http://localhost_

| Method                        | HTTP request                   | Description |
| ----------------------------- | ------------------------------ | ----------- |
| [**createTask**](#createtask) | **POST** /api/task             | Create Task |
| [**deleteTask**](#deletetask) | **DELETE** /api/task/{task_id} | Delete Task |
| [**getTask**](#gettask)       | **GET** /api/task/{task_id}    | Get Task    |
| [**listTasks**](#listtasks)   | **GET** /api/task              | List Tasks  |
| [**updateTask**](#updatetask) | **PUT** /api/task/{task_id}    | Update Task |

# **createTask**

> Task createTask(createTask)

Create a new task for the current user.

### Example

```typescript
import { TaskApi, Configuration, CreateTask } from "./api";

const configuration = new Configuration();
const apiInstance = new TaskApi(configuration);

let createTask: CreateTask; //

const { status, data } = await apiInstance.createTask(createTask);
```

### Parameters

| Name           | Type           | Description | Notes |
| -------------- | -------------- | ----------- | ----- |
| **createTask** | **CreateTask** |             |       |

### Return type

**Task**

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

# **deleteTask**

> deleteTask()

Delete a task by ID.

### Example

```typescript
import { TaskApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new TaskApi(configuration);

let taskId: string; // (default to undefined)

const { status, data } = await apiInstance.deleteTask(taskId);
```

### Parameters

| Name       | Type         | Description | Notes                 |
| ---------- | ------------ | ----------- | --------------------- |
| **taskId** | [**string**] |             | defaults to undefined |

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

# **getTask**

> Task getTask()

Retrieve a task by ID.

### Example

```typescript
import { TaskApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new TaskApi(configuration);

let taskId: string; // (default to undefined)

const { status, data } = await apiInstance.getTask(taskId);
```

### Parameters

| Name       | Type         | Description | Notes                 |
| ---------- | ------------ | ----------- | --------------------- |
| **taskId** | [**string**] |             | defaults to undefined |

### Return type

**Task**

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

# **listTasks**

> Array<Task> listTasks()

Retrieve all tasks for the current user.

### Example

```typescript
import { TaskApi, Configuration } from "./api";

const configuration = new Configuration();
const apiInstance = new TaskApi(configuration);

const { status, data } = await apiInstance.listTasks();
```

### Parameters

This endpoint does not have any parameters.

### Return type

**Array<Task>**

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

# **updateTask**

> Task updateTask(updateTask)

Update a task by ID.

### Example

```typescript
import { TaskApi, Configuration, UpdateTask } from "./api";

const configuration = new Configuration();
const apiInstance = new TaskApi(configuration);

let taskId: string; // (default to undefined)
let updateTask: UpdateTask; //

const { status, data } = await apiInstance.updateTask(taskId, updateTask);
```

### Parameters

| Name           | Type           | Description | Notes                 |
| -------------- | -------------- | ----------- | --------------------- |
| **updateTask** | **UpdateTask** |             |                       |
| **taskId**     | [**string**]   |             | defaults to undefined |

### Return type

**Task**

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
