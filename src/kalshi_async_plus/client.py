import asyncio
import logging
import sys
from typing import List, Any, Optional
from kalshi_python_async import KalshiClient as BaseKalshiClient
from kalshi_async_plus.constants import Sport

# Set up a logger for the "Plus" features
logger = logging.getLogger("kalshi_async_plus")

class KalshiClient(BaseKalshiClient):
    """
    A drop-in replacement for the official KalshiClient.
    Inherits all functionality and adds missing convenience methods.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Link our logger so it respects the official config.debug flag
        self.configuration.logger["plus_logger"] = logger
        
        if self.configuration.debug:
            logger.setLevel(logging.DEBUG)
            # If no handlers exist, add a simple console handler so debug prints actually appear
            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
                logger.addHandler(handler)
        else:
            logger.setLevel(logging.WARNING)

    async def get_all_events(self, sport: Optional[Sport] = None, **kwargs: Any) -> List[Any]:
        """
        Automatically handles pagination/cursors to return a complete list of events.
        
        If `sport` is provided, it filters the results strictly against 
        the official competition list returned by the Kalshi Search API.
        """
        official_competitions = None
        
        # 1. Fetch official filters if a sport is specified
        if sport:
            logger.debug(f"Filtering events for sport: {sport}")
            try:
                filters_resp = await self.get_filters_for_sports()
                sport_match = next(
                    (s for s in filters_resp.filters_by_sports if s.lower() == sport.value.lower()), 
                    None
                )
                
                if not sport_match:
                    logger.warning(f"Sport '{sport}' not found in official filters.")
                    return []
                
                details = filters_resp.filters_by_sports[sport_match]
                official_competitions = {k.lower() for k in details.competitions.keys()}
                
            except Exception as e:
                logger.error(f"Failed to fetch official sport filters: {e}")
                return []

        # 2. Standard pagination logic for fetching pages of events
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
        
        # 3. Apply Sport filtering if requested
        if official_competitions is not None:
            filtered = [
                event for event in all_events
                if (getattr(event, 'product_metadata', {}) or {}).get('competition', '').lower() in official_competitions
            ]
            logger.debug(f"Metadata Filter: Found {len(filtered)} events for {sport}.")
            return filtered
                
        return all_events
