# Personalised Error Raises
class WrongCoinCode(NotImplementedError):
    """This coin code is unavailable at 'coinmarketcap.com'"""


class CoinMarketCapDown(ConnectionError):
    """ CoinMarketCap API is down. Try later"""


class BadSnapshotURL(ConnectionError):
    """Check 'https://coinmarketcap.com/historical/' for available historical snapshot periods"""
