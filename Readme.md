# Description
This is a core library for PriceLab. It provides a set of tools for building PriceLab microservices. 
It includes a set of common functionality. 

- Infrastructure such as logging, telemetry, configuration, Http client, serialization and more.
- Business logic such as domain models, validation shared among microservices.

# Installation
To install the latest version of the library, run the following command:

```bash
pip install pricelab-core
```

To install the latest version of the library from the test PyPI repository, run the following command:

```bash
pip install -i https://test.pypi.org/simple/ pricelab-core
```

> [!WARNING]
> The test version of the library is for testing purposes only and is not intended for use in production.

## Example Usage
The following example demonstrates how to use the library to create a simple resilient http client, that will have:

- Base http client (async)
- Retry
- Circuit breaker
- Telemetry

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
