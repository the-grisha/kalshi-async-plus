# kalshi-async-plus

An extended, drop-in replacement for the official [kalshi-python-async](https://pypi.org/project/kalshi-python-async/) SDK, featuring the methods you were missing so much.

## Installation

```bash
uv add kalshi-async-plus
```

## Plus Features

### 1. Cleaner Configuration
Pass your credentials directly into the `Configuration` constructor—no more manual attribute assignment.

```python
from kalshi_async_plus import Configuration, KalshiClient

config = Configuration(
    api_key_id="your_id",
    private_key_pem="your_pem_string",
    debug=True  # Automatically enables Plus-level debug logging
)
client = KalshiClient(config)
```

### 2. High-Precision Sport Filtering
Fetch events for specific sports with perfect parity to the Kalshi website. Our `get_all_events` method handles pagination and official metadata filtering for you.

```python
from kalshi_async_plus import KalshiClient, Sport

async def main():
    async with KalshiClient(config) as client:
        # Uses the Sport enum for type-safety and auto-completion
        baseball_events = await client.get_all_events(sport=Sport.BASEBALL, status="open")
        
        for event in baseball_events:
            print(f"Baseball Game: {event.title}")
```

### 3. Linked Debugging
When you set `debug=True` in your configuration, `kalshi-async-plus` automatically activates its internal high-level logging to show you exactly how your filters and pagination are performing.
