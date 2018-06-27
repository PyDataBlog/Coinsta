"""coinsta - A Python package for acquiring both historical and current data of cryptocurrencies"""

__version__ = '0.0.1'
__author__ = 'Bernard Brenyah <bbrenyah@gmail.com>'
__all__ = []

from .core import Historical, Current
from .exceptions import WrongCoinCode
