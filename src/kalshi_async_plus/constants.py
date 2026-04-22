from enum import Enum

class Sport(str, Enum):
    """
    List of sport categories available on Kalshi.
    Feel free to add missing sports
    """
    BASEBALL = "Baseball"
    BASKETBALL = "Basketball"
    SOCCER = "Soccer"
    TENNIS = "Tennis"
