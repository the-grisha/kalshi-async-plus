import asyncio
import logging
from typing import List, Any, Optional, Union
from kalshi_python_async import KalshiClient as BaseKalshiClient
from kalshi_async_plus.constants import Sport, Scope

# Set up a logger for the "Plus" features
logger = logging.getLogger("kalshi_async_plus")

class KalshiClient(BaseKalshiClient):
    """
    A drop-in replacement for the official KalshiClient.
    Inherits all functionality and adds missing convenience methods.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Link our logger so it respects the official config.debug flag.
        # We don't add handlers here to avoid double-logging; we rely on 
        # the user's standard logging configuration (e.g. logging.basicConfig).
        self.configuration.logger["plus_logger"] = logger
        
        if self.configuration.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

    async def get_all_events(
        self, 
        sport: Optional[Sport] = None, 
        scope: Optional[Union[Scope, List[Scope]]] = None,
        **kwargs: Any
    ) -> List[Any]:
        """
        Automatically handles pagination/cursors to return a complete list of events.
        
        If `sport` is provided, it filters by official competition metadata.
        If `scope` is provided, it filters by competition scope.
        """
        official_competitions = None
        target_scopes = None
        
        # 1. Prepare Sport Filter
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

        # 2. Prepare Scope Filter
        if scope:
            if isinstance(scope, Scope):
                target_scopes = {scope.value.lower()}
            else:
                target_scopes = {s.value.lower() for s in scope}

        # 3. Standard pagination logic for fetching pages of events
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
        
        # 4. Apply Filters
        filtered_events = all_events
        
        if official_competitions is not None or target_scopes is not None:
            final_list = []
            for event in all_events:
                metadata = getattr(event, 'product_metadata', {}) or {}
                
                # Check sport parity
                sport_match = True
                if official_competitions is not None:
                    event_comp = (metadata.get('competition') or "").lower()
                    sport_match = event_comp in official_competitions
                
                # Check scope parity (handles common plural/singular API inconsistencies)
                scope_match = True
                if target_scopes is not None:
                    event_scope = (metadata.get('competition_scope') or "").lower()
                    scope_match = any(
                        event_scope == ts or 
                        event_scope == ts.rstrip('s') or 
                        event_scope + 's' == ts
                        for ts in target_scopes
                    )
                
                if sport_match and scope_match:
                    final_list.append(event)
            
            filtered_events = final_list
            logger.debug(f"Filter Results: {len(filtered_events)} events matched (Sport: {sport}, Scope: {scope})")
                
        return filtered_events
