# Machine Learning pipelines

This document provides a summary of key concepts related to Machine Learning Operations (MLOps) and workflow orchestration with Prefect.

## What is an ML Pipeline?
An ML Pipeline is a sequence of automated steps designed to train and prepare a machine learning model for a production environment. In essence, it's a structured way to execute a series of scripts or tasks in a specific order to produce a trained, production-ready model.

## Workflow Orchestration with Prefect
Prefect is a tool used to orchestrate and manage complex workflows, such as ML pipelines. It allows you to move from running workflows manually to managing them on a remote server with a UI and API.

## Prefect Deployments
A deployment in Prefect encapsulates the metadata and configuration required to orchestrate a workflow. It specifies when, where, and how a workflow should run, without storing the actual code. This information is typically stored in a prefect.yaml file.

### Key Benefits:

**Remote Management**: Trigger, schedule, and manage flows from a UI or API.\
**Scheduling**: Set up automated runs at specific times or intervals.\
**Automation**: Trigger workflows based on external events.\
**Dynamic Infrastructure**: Define the specific infrastructure (e.g., local process, Docker container, cloud instance) where the flow will execute.\


## Type of deployment
There are two main types of deployments:

**Static Deployment**: Uses the .serve() method to start an agent that listens for work and executes flow runs in subprocesses. This gives you full control over the execution environment and is suitable for simple, frequent pipelines.\
**Dynamic Deployment**: Leverages Work Pools and Workers. This approach allows for dynamically provisioning infrastructure, which is cost-effective for infrequent, resource-intensive tasks like training a deep learning model.
Work Pools and Workers.\

In a dynamic deployment, runs are submitted to a **Work Pool**. A **Worker** is a process that polls the work pool for scheduled runs and executes them on the configured infrastructure.

A critical rule is that the **worker's type must match the work pool's type**. For example, a work pool configured to use Docker requires a Docker worker. This ensures that the flow runs are executed in the correct environment, allowing infrastructure to evolve with the flow's requirements (e.g., moving from a local Docker container to a more powerful cloud-based environment like Google Vertex AI).

## Work Pools

A Work Pool in Prefect is analogous to a topic in a pub/sub system. It acts as a channel between deployments and workers, enabling dynamic infrastructure provisioning. Deployments publish flow runs to a work pool, and workers subscribe to that pool to execute the runs on the specified infrastructure.

## Work pools are categorized into three types:

**Hybrid**: A worker in your infrastructure submits runs to your infrastructure.\
**Push**: Runs are automatically submitted to your configured serverless infrastructure provider.\
**Managed**: Runs are automatically submitted to Prefect-managed infrastructure.\

Each category has different types, and each type corresponds to a specific infrastructure. The worker's type must match the work pool's type to ensure proper execution.