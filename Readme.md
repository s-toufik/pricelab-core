# Description

This is a core library for PriceLab, providing a shared foundation for building microservices.
It offers reusable components organized into two main areas:

### Infrastructure
Common technical capabilities used across services, including:

- Logging
- Telemetry and observability
- Configuration management
- HTTP client utilities
- Serialization and deserialization
- ...

### Business Logic
Shared domain-level building blocks, including:

- Core domain models
- Validation rules and utilities
- Cross-service business abstractions

# Installation

To install the latest stable version of the library:

```bash
pip install pricelab-core
```

Test environment installation

To install the latest version from the Test PyPI repository:

```bash
pip install -i https://test.pypi.org/simple/ pricelab-core
```

> [!WARNING]
> The Test PyPI version includes the latest features but may not be stable. It is intended for development and testing purposes only and should not be used in production environments.

## Example Usage

The following example demonstrates how to use the library to create a simple resilient HTTP client with the following capabilities:

- Asynchronous base HTTP client
- Retry mechanism
- Circuit breaker pattern
- Telemetry and observability integration

```python
    base_client: HttpClient = AioHttpClient(
        base_url="https://www.alphavantage.co",
    )
    
    retry_policy: Retry = RetryPolicy(
        RetrySettings()
    )
    
    circuit_breaker: CircuitBreakerPolicy = CircuitBreakerPolicy(
        CircuitBreakerSettings()
    )
    
    telemetry: Telemetry = OpenTelemetryManager(service_name="alpha-vantage")
    
    client: ResilientHttpClient = ResilientClient(
        base_client=base_client,
        circuit_breaker=circuit_breaker,
        retry_policy=retry_policy,
        trace_manager=telemetry,
    )
    
    try:
        await base_client.start()
    
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": "IBM",
            "interval": "5min",
            "apikey": "demo",
        }
    
        response = await client.get(
            "/query",
            params=params,
        )
    
        print(response)
    finally:
        await base_client.close()
        telemetry.shutdown()
```
