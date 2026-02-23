# 3. RabbitMQ for communcation between REST API and sched/sync worker

Date: 2026-02-12

## Status

Accepted

## Context

The REST API and the sched/sync worker need to communicate to coordinate scheduling and synchronization tasks. We need a reliable and efficient way for these two components to exchange information about task statuses, scheduling requests, and other relevant data.

## Decision

PostgreSQL is not suitable for this task as its LISTEN/NOTIFY mechanism is not designed for high-throughput, low-latency communication between components.
Instead, we will use RabbitMQ as a message broker to enable communication between the REST API and the sched/sync worker.
RabbitMQ provides robust messaging capabilities, including support for various messaging patterns, reliable delivery, and scalability.

## Consequences

- The REST API and sched/sync worker will need to implement RabbitMQ clients to send and receive messages.
- We will need to set up and maintain a RabbitMQ server as part of our infrastructure.
- This approach will allow for more efficient and scalable communication between the components, improving overall system performance and reliability.
- We will need to ensure that the message formats and protocols are well-defined to ensure smooth communication between the REST API and the sched/sync worker.
