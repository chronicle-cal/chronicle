# Rule

## Properties

| Name           | Type                                       | Description | Notes                             |
| -------------- | ------------------------------------------ | ----------- | --------------------------------- |
| **id**         | **number**                                 |             | [default to undefined]            |
| **source_id**  | **string**                                 |             | [default to undefined]            |
| **enabled**    | **boolean**                                |             | [default to undefined]            |
| **name**       | **string**                                 |             | [default to undefined]            |
| **conditions** | [**Array&lt;Condition&gt;**](Condition.md) |             | [optional] [default to undefined] |
| **actions**    | [**Array&lt;Action&gt;**](Action.md)       |             | [optional] [default to undefined] |

## Example

```typescript
import { Rule } from "./api";

const instance: Rule = {
  id,
  source_id,
  enabled,
  name,
  conditions,
  actions,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
