# ML Project Lifecycle & Deployment Overview

This document outlines the typical phases of an ML project and the options available for deploying trained models based on prediction latency requirements.

![deployment options](../assets/different%20ml%20model%20deployments%20modes.png)
---

## 📌 ML Project Phases

1. **Design**
   - Understand and frame the problem.
   - Decide that Machine Learning is the appropriate solution.

2. **Train**
   - Build an experiment tracking system.
   - Implement a training pipeline.
   - Output: A production-ready **ML model**.

3. **Operate**
   - Deploy the trained model to production.

---

## 🚀 Deployment Strategies

Before deploying, ask:
> ❓ Do we need predictions immediately, or can we wait (hour/day/week/month)?

### 1. **Batch Deployment (Offline Mode)**
- Suitable when **immediate predictions aren't required**.
- The model is **not continuously running**.
- New data is processed **periodically** (e.g., daily, hourly, weekly).

### 2. **Online Deployment (Real-Time Mode)**
- Required when **predictions must be instant**.
- The model is **continuously available** and responds to real-time queries.

#### Online deployment modes:
- **Web Service**: Exposes the model via an API (e.g., REST).
- **Streaming**: Model consumes data streams and returns real-time predictions.

---

Choose the appropriate deployment mode based on your application's latency requirements.







