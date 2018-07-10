"""coinsta - A Python package for acquiring both historical and current data of cryptocurrencies"""


from .core import Historical, Current
from .exceptions import WrongCoinCode
from pkg_resources import get_distribution

__version__ = get_distribution('coinsta').version
__author__ = 'Bernard Brenyah <bbrenyah@gmail.com>'
__all__ = []