# Task

## Properties

| Name            | Type                                        | Description | Notes                             |
| --------------- | ------------------------------------------- | ----------- | --------------------------------- |
| **id**          | **string**                                  |             | [default to undefined]            |
| **completed**   | **boolean**                                 |             | [default to undefined]            |
| **title**       | **string**                                  |             | [default to undefined]            |
| **description** | **string**                                  |             | [default to undefined]            |
| **due_date**    | **string**                                  |             | [optional] [default to undefined] |
| **duration**    | **number**                                  |             | [optional] [default to 30]        |
| **not_before**  | **string**                                  |             | [optional] [default to undefined] |
| **priority**    | **number**                                  |             | [optional] [default to 3]         |
| **profile**     | [**ProfileReadShort**](ProfileReadShort.md) |             | [optional] [default to undefined] |

## Example

```typescript
import { Task } from "./api";

const instance: Task = {
  id,
  completed,
  title,
  description,
  due_date,
  duration,
  not_before,
  priority,
  profile,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
