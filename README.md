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

### 2. High-Precision Sport & Scope Filtering
Fetch events with perfect parity to the Kalshi website using type-safe enums.

```python
from kalshi_async_plus import KalshiClient, Sport, Scope

async def main():
    async with KalshiClient(config) as client:
        # 1. Fetch all baseball games
        baseball_events = await client.get_all_events(
            sport=Sport.BASEBALL, 
            status="open"
        )
        
        # 2. Granular filtering: Just Tennis "Games" (skips Futures/Set Winners)
        tennis_games = await client.get_all_events(
            sport=Sport.TENNIS,
            scope=Scope.GAMES,
            status="open"
        )
        
        for event in tennis_games:
            print(f"Match: {event.title}")
```

### 3. Professional Logging & Debugging
When you set `debug=True` in your configuration, `kalshi-async-plus` automatically activates its internal high-level logging. We've cleaned up propagation so you get clean, singular log entries in your console.
