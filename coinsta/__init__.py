"""coinsta - A Python package for acquiring both historical and current data of cryptocurrencies"""


from .core import Historical, Current
from .exceptions import WrongCoinCode

__version__ = '0.1.2'
__author__ = 'Bernard Brenyah <bbrenyah@gmail.com>'
__all__ = []
