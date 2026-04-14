# kalshi-async-plus

An extended, drop-in replacement for the official [kalshi-python-async](https://pypi.org/project/kalshi-python-async/) SDK, featuring the methods you were missing so much.

## Installation

```bash
uv add kalshi-async-plus
```

## Usage

Use it as a seamless replacement for the official SDK.

```python
import asyncio
from kalshi_async_plus import KalshiClient, Configuration

async def main():
    # Use exactly like the official SDK
    config = Configuration(
        api_key_id="your_api_key_id",
        private_key_pem="your_private_key_pem"
    )
    client = KalshiClient(config)
    
    # But with extra methods you were missing!
    # Automatically handles pagination to get every single event
    all_events = await client.get_all_events()
    print(f"Found {len(all_events)} events")

if __name__ == "__main__":
    asyncio.run(main())
```
