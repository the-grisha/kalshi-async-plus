from typing import List, Any
from kalshi_python_async import KalshiClient as BaseKalshiClient

class KalshiClient(BaseKalshiClient):
    """
    A drop-in replacement for the official KalshiClient.
    Inherits all functionality and adds missing convenience methods.
    """
    
    async def get_all_events(self, **kwargs: Any) -> List[Any]:
        """
        Automatically handles pagination/cursors to return a complete list of events.
        """
        all_events = []
        cursor = None
        
        while True:
            if cursor:
                kwargs['cursor'] = cursor
            
            response = await self.get_events(**kwargs)
            all_events.extend(response.events)
            
            cursor = getattr(response, 'cursor', None)
            if not cursor:
                break
                
        return all_events
