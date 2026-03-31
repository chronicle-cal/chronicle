# CreateTask

## Properties

| Name            | Type       | Description | Notes                             |
| --------------- | ---------- | ----------- | --------------------------------- |
| **title**       | **string** |             | [default to undefined]            |
| **description** | **string** |             | [optional] [default to undefined] |
| **due_date**    | **string** |             | [optional] [default to undefined] |
| **duration**    | **number** |             | [optional] [default to 30]        |
| **not_before**  | **string** |             | [optional] [default to undefined] |
| **priority**    | **number** |             | [optional] [default to 3]         |
| **profile_id**  | **string** |             | [optional] [default to undefined] |

## Example

```typescript
import { CreateTask } from "./api";

const instance: CreateTask = {
  title,
  description,
  due_date,
  duration,
  not_before,
  priority,
  profile_id,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
