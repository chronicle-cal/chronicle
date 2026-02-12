# 2. Calendar synchronisation and scheduling as microservice

Date: 2026-02-12

## Status

Accepted

## Context

It is up for debate on how to handle calendar synchronisation and scheduling in Chronicle. The two main options are:

1. Implement calendar synchronisation and scheduling as part of the core Chronicle service, which would be responsible for managing all aspects of a user's schedule and calendar.

2. Implement calendar synchronisation and scheduling as a separate microservice, which would be responsible for managing the user's schedule and calendar, and would communicate with the core Chronicle service to provide scheduling information and updates.

The main benefit of option 1 is that it would allow for tighter integration between the scheduling and calendar features and the rest of the Chronicle service.

The main downside of option 1 is that it would make the core Chronicle service more complex and harder to maintain, as it would need to handle both scheduling and calendar management in addition to its other responsibilities. Additionally, the sychronisation with external servies and the scheduling logic itself are both complex and take long to run and could be better isolated in a separate service.

## Decision

We will implement calendar synchronisation and scheduling as a separate microservice, which will be responsible for managing the user's schedule and calendar, and will communicate with the core Chronicle service to provide scheduling information and updates.

## Consequences

This decision will allow for better separation of concerns and modularity in the overall architecture of Chronicle. It will also allow for easier maintenance and scalability of the scheduling and calendar features, as they will be isolated in a separate service. However, it will require additional effort to implement the communication between the core Chronicle service and the scheduling microservice, and may introduce some latency in providing scheduling information to the user.
