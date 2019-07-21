# Personalised Error Raises
class WrongCoinCode(NotImplementedError):
    """This coin code is unavailable at 'coinmarketcap.com'"""


class BadSnapshotURL(ConnectionError):
    """Check 'https://coinmarketcap.com/historical/' for available historical snapshot periods"""
