# Documentation

## Summary
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Example Usage](#example-usage)

---

# Description

`pricelab-core` is the foundational shared library of the PriceLab ecosystem.

It provides reusable infrastructure and domain components that standardize the development of microservices and internal services across the platform.

The library is designed with a strong focus on:

- Modularity
- Reusability
- Maintainability

---

# Features

The library is organized into two primary domains:

- [Infrastructure](#infrastructure)
- [Business Logic](#business-logic)

---

# Infrastructure

Infrastructure modules provide reusable technical capabilities shared across services.

## Included Components

### Logging

Provides standardized and structured logging utilities.

Features:
- Structured logs

---

### Telemetry and Observability

Provides integration with observability platforms.

Features:
- Distributed tracing
- Metrics collection
- OpenTelemetry integration
- Request lifecycle tracking
- Error monitoring

---

### Configuration Management

Provides centralized and environment-driven configuration handling.

Features:
- YAML configuration support
- Environment variable injection
- Typed configuration models
- Validation utilities

---

### HTTP Client Utilities

Provides resilient and extensible HTTP communication utilities.

Features:
- Asynchronous HTTP clients
- Retry policies
- Circuit breaker integration
- Timeout management
- Request tracing
- Fault tolerance

---

### Serialization and Deserialization

Provides utilities for object transformation and schema handling.

Features:
- JSON/HashMap/Binary serialization/deserialization
- Typed model conversion
- Schema validation
- DTO mapping

---

# Business Logic

Business modules provide reusable domain-oriented abstractions.

## Included Components

### Core Domain Models

Shared business entities and value objects used across services.

Examples:
- Candles/Quotes
- Time-series
- Pricing models

---

### Validation Utilities

Provides reusable validation mechanisms.

Features:
- Schema validation
- Business rule enforcement
- Constraint validation

---

# Installation

## Stable Version

Install the latest stable version from PyPI:

```bash
pip install pricelab-core
```

---

## Test Environment Installation

Install the latest development version from the Test PyPI repository:

```bash
pip install -i https://test.pypi.org/simple/ pricelab-core
```

> [!WARNING]
> The Test PyPI version includes the latest experimental features and improvements but may not be stable.
> It is intended exclusively for development and testing purposes and should **not** be used in production environments.

---

# Example Usage

The following example demonstrates how to build a resilient asynchronous HTTP client using:

- Asynchronous HTTP communication
- Retry mechanisms
- Circuit breaker protection
- Telemetry and observability integration

---

## Architecture Overview

```text
                    +----------------------+
                    |  Resilient Client    |
                    +----------+-----------+
                               |
         +---------------------+---------------------+
         |                     |                     |
         ▼                     ▼                     ▼
+----------------+   +----------------+   +----------------+
| Retry Policy   |   | CircuitBreaker |   | Telemetry      |
+----------------+   +----------------+   +----------------+
                               |
                               ▼
                    +----------------------+
                    |  Async HTTP Client   |
                    +----------+-----------+
                               |
                               ▼
                    +----------------------+
                    | External API Service |
                    +----------------------+
```

---

## Complete Example

```python
# Create the base asynchronous HTTP client
base_client = AioHttpClient(base_url="<base url>")

# Configure retry policy
retry_policy = RetryPolicy(
    RetrySettings(max_attempts=3, delay_seconds=1)
)

# Configure circuit breaker
circuit_breaker = CircuitBreakerPolicy(
    CircuitBreakerSettings(failure_threshold=5, recovery_timeout=30)
)

# Configure telemetry
telemetry = OpenTelemetryManager(service_name="<external api name>")

# Create resilient HTTP client
client = ResilientClient(
    base_client=base_client,
    circuit_breaker=circuit_breaker,
    retry_policy=retry_policy,
    trace_manager=telemetry,
)

async def fetch_intraday_stock() -> None:
    try:
        await client.start()

        params = {
            "function": "<function name>",
            "symbol": "<stock symbol>",
            "interval": "<time interval>",
            "apikey": "<api key>",
        }

        response = await client.get("/<endpoint>", params=params)

        print(response)

    finally:
        # Gracefully shutdown resources
        await client.close()
        telemetry.shutdown()
```
