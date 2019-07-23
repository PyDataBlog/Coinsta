# Personalised Error Raises
class WrongCoinCode(NotImplementedError):
    """This coin code is unavailable at 'coinmarketcap.com'"""


class BadSnapshotURL(ConnectionError):
    """Check 'https://coinmarketcap.com/historical/' for available historical snapshot periods"""


class ApiKeyError(KeyError):
    """ API Key reject by CoinMarketCap API Check 'https://pro.coinmarketcap.com/signup/' for a valid API Key"""
