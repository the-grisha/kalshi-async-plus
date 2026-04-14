# Re-export everything from the official SDK
from kalshi_python_async import *

# Override the KalshiClient with our version
from kalshi_async_plus.client import KalshiClient

# Ensure __all__ includes our KalshiClient if we want to be explicit, 
# though 'from kalshi_python_async import *' will import everything.
# Let's keep it simple for the drop-in replacement goal.
