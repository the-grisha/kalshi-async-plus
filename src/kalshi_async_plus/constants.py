from enum import Enum

class Sport(str, Enum):
    """
    List of sport categories available on Kalshi.
    """
    BASEBALL = "Baseball"
    BASKETBALL = "Basketball"
    SOCCER = "Soccer"
    TENNIS = "Tennis"

class Scope(str, Enum):
    """
    Common competition scopes available on Kalshi.
    """
    EVENTS = "Events"
    GAMES = "Games"
    FUTURES = "Futures"
