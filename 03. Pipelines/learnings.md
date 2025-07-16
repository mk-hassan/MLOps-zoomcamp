# Machine Learning Pipelines with Prefect: Learnings

This document summarizes the key learnings from each Python script in this module, tracking the progression from basic to more advanced Prefect concepts.

## 01_basic_example_with_flows.py

This script introduces the most fundamental concept in Prefect: the **flow**. 

**Key Learning:**

*   A flow is the basic unit of execution in Prefect, representing a single pipeline run.
*   You can define a flow by decorating a Python function with `@flow`.
*   A flow can be executed like any other Python function.

This first example demonstrates the simplest possible Prefect application, laying the groundwork for more complex pipelines.

## 02_flows_and_tasks.py

This script introduces the concept of a **task** within a flow.

**Key Learnings:**

*   A **task** is a distinct unit of work within a flow. You can define a task by decorating a Python function with `@task`.
*   Tasks can be called from within a flow, and their results can be used by other tasks or by the flow itself.
*   This allows for modular and reusable code within your pipelines.

## 03_sync_demo.py

This script demonstrates the default **synchronous** execution of tasks within a Prefect flow.

**Key Learning:**

*   By default, tasks within a flow are executed sequentially. Each task waits for the previous one to complete before it begins.
*   This is useful for workflows where the output of one task is the direct input for the next, and there's a strict order of operations.
*   The `time.sleep()` calls are used to simulate tasks that take a significant amount of time to run, making the synchronous behavior more apparent.

## 04_async_demo_with_submit.py

This script introduces **asynchronous** task execution using the `.submit()` method.

**Key Learnings:**

*   To run tasks concurrently, you can use the `.submit()` method when calling a task. This immediately returns a `PrefectFuture` object, and the task starts running in the background.
*   This is ideal for tasks that are independent of each other and can be executed in parallel, significantly speeding up the total runtime of the flow.
*   To get the actual result of a submitted task, you need to call the `.result()` method on the future. This will block until the task is complete.

## 05_async_sync_mixed_demo.py

This script demonstrates a more realistic scenario where a flow combines both **synchronous and asynchronous** patterns.

**Key Learnings:**

*   Real-world pipelines often have a mix of tasks that can run in parallel and tasks that have dependencies.
*   You can use `.submit()` for independent tasks to run them asynchronously.
*   When a task depends on the output of a submitted task, you call `.result()` on the future to get the result and pass it to the dependent task. This creates a point of synchronization in the flow.

## 06_retry_logic.py

This script introduces the concept of **retries** for tasks that might fail intermittently.

**Key Learnings:**

*   You can make tasks more resilient by configuring them to retry on failure. This is done by passing the `retries` and `retry_delay_seconds` arguments to the `@task` decorator.
*   In this example, the `fetch_user_info` task is set to retry up to 3 times, with a 5-second delay between each attempt.
*   This is a crucial feature for building robust pipelines that can handle transient errors in external systems or services.

## 07_retry_logger.py

This script adds **logging** to the pipeline, which is essential for monitoring and debugging.

**Key Learnings:**

*   Prefect has a built-in logging mechanism that can be accessed by calling `get_run_logger()` within a flow or task.
*   You can use the logger to record important information, warnings, and errors throughout the execution of your pipeline.
*   This is invaluable for understanding what your flows are doing, especially when they are running in the background or on a schedule.

## 08_sync_async_retry_logger.py

This script combines all the concepts learned so far: **synchronous and asynchronous execution, retries, and logging**.

**Key Learning:**

*   This example represents a more complete and robust pipeline.
*   It demonstrates how to structure a flow with a mix of dependent and independent tasks.
*   It uses `.submit()` for parallelism, `.result()` for synchronization, `@task(retries=...)` for resilience, and `get_run_logger()` for observability.
*   This is a solid template for building real-world data pipelines with Prefect.

## 09_user_flow.py

This script introduces the concept of **serving** a flow, which makes it available as a long-running process that can be triggered on demand.

**Key Learnings:**

*   The `.serve()` method on a flow creates a deployment for that flow.
*   A served flow runs in the background and can be triggered manually or by a schedule.
*   This is a key step towards productionizing your pipelines, as it allows them to be managed and executed without needing to manually run the Python script each time.

## 10_trigger_deploymnet_by_id.py

This script demonstrates how to **trigger a deployed flow** using its ID.

**Key Learnings:**

*   Once a flow is deployed (e.g., using `.serve()`), it can be triggered by making an API call to the Prefect server.
*   This script uses the `requests` library to send a POST request to the `/api/deployments/{deployment_id}/create_flow_run` endpoint.
*   You can pass parameters to the flow run in the JSON payload of the request.
*   This enables programmatic triggering of your pipelines from other applications or services.

## 11_get_deployment_id_by_name.py

This script shows how to **dynamically retrieve a deployment's ID** using its flow and deployment name.

**Key Learnings:**

*   Hardcoding deployment IDs is not ideal, as they can change. A better approach is to look them up by name.
*   This script defines a function that makes a GET request to the `/api/deployments/name/{flow_name}/{deployment_name}` endpoint.
*   This allows you to decouple your triggering logic from specific deployment IDs, making your code more robust and maintainable.

## 12_trigger_deploymnet_by_id_name_lookup.py

This script combines the previous two concepts to create a complete, robust triggering mechanism.

**Key Learnings:**

*   It first dynamically fetches the deployment ID by its flow and deployment name.
*   Then, it uses that ID to trigger a new flow run, passing in the required parameters.
*   This represents a best-practice approach for programmatically interacting with Prefect deployments, as it is both flexible and resilient to changes in the environment.
