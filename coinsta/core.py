# needed libraries
import pandas as pd
import requests
from coinsta.exceptions import CoinMarketCapDown, BadSnapshotURL
from coinsta.utils import _readable_date, _ticker_checker, _snapshot_readable_date
from datetime import date, datetime


# Historical Class for all methods related to historical data
class Historical:
    """
    A class that provides methods for scraping historical price data
    based on specified crypto-currencies and time period from
    CoinMarketCap.
    """

    def __init__(self, ticker, start, end=None):
        """
        This method initialises the Historical object based on the
        ticker, starting period, and ending period as specified by
        users.

        :param ticker: str object representing ticker information.
        :param start: a Datetime date object representing YYYYMMDD.
        :param end: a Datetime date object representing YYYYMMDD.
        """

        # Check for mis-specification of dates
        if isinstance(start, date) is False:
            raise TypeError("Start argument must be a date object or strings with the alternative 'from_strings' "
                            "constructor")

        # Convert start day into to appropriate format for scraping data from CoinMarketCap
        start = start.isoformat().replace("-", "")

        # Use today's date unless otherwise specified by user
        if end is None:
            today = date.today()
            formatted_today = today.isoformat().replace("-", "")
            end = formatted_today
        elif isinstance(end, date) is False:
            raise TypeError("End argument must be a date object or \
                                        strings with the alternative 'from_strings' constructor")
        else:
            end = end.isoformat().replace("-", "")

        # Self assign default args
        self.ticker = ticker
        self.start = start
        self.end = end

    def __repr__(self):
        return "<Historical({0}, {1}, {2})>".format(self.ticker, self.start, self.end)

    def __str__(self):
        return "Coinsta object: \n crypto_symbol: {0} \n start_period: {1} \n" \
               " end_period: {2}".format(self.ticker,
                                         _readable_date(self.start),
                                         _readable_date(self.end)
                                         )

    def get_data(self):
        """
        This function scrapes and cleans the data of the specified tickers
        from CoinMarketCap website.

        :return: A Pandas DataFrame object containing historical data on the specified tickers.
        """

        # Get the ticker id used by CoinMarketCap
        slug = _ticker_checker(self.ticker)

        # Custom data url based on the user specified ticker and starting period and ending period
        site_url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(slug,
                                                                                                        self.start,
                                                                                                        self.end)
        # Download the data based on the custom data url
        data = pd.read_html(site_url)
        df = data[0]
        df['Date'] = pd.to_datetime(df['Date'])

        df.rename(
            {
                "Open*": "Open",
                "Close**": "Close",
                "Market Cap": "Market_cap"
            },
            axis='columns', inplace=True
        )

        df.set_index('Date', drop=True, inplace=True)
        df.sort_index(inplace=True)
        return df

    @classmethod
    def from_strings(cls, ticker, start, end, hyphen=True):
        """
        An alternative constructor that accepts strings
        string format YYYY-MM-DD or YYYY/MM/DD.
        Default format is the hyphen separate string: YYYY-MM-DD.
        Turn `hyphen` to False if string to be parsed is: YYYY/MM/DD.

        :param ticker: A str object specifying the ticker information
        :param start: A str object specifying the starting period under consideration.
        :param end: A str object specifying the ending period under consideration.
        :param hyphen: A boolean object indicating the separator in the start/end str is "-" or "/". Default is "-".

        :return: A Pandas DataFrame object containing historical data on the specified ticker.
        """

        if hyphen:
            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()
        else:
            start = datetime.strptime(start, "%Y/%m/%d").date()
            end = datetime.strptime(end, "%Y/%m/%d").date()

        return cls(ticker, start, end)


# A class that handles historical snapshots of crypto markets
class HistoricalSnapshot:
    """
    A class that returns a historical snapshot of crypto-currency market information
    on a specified period of time.
    """

    def __init__(self, period):
        assert isinstance(period, date)
        self.period = period

    def __repr__(self):
        return "<HistoricalSnapshot({0})>".format(self.period)

    def __str__(self):

        return "CoinMarketCap Historical Snapshot for the period: {0}".format(_snapshot_readable_date(self.period))

    def get_snapshot(self):
        """
        A method the retrieves a historical snapshot of crypto-currency markets via CoinMarketCap.

        :return: A Pandas DataFrame object with historical snapshot data of the period specified.
        """
        snap_date = self.period.isoformat().replace("-", "")
        snap_url = "https://coinmarketcap.com/historical/{0}".format(snap_date)

        check_snap = requests.get(snap_url)
        if check_snap.status_code != 200:
            raise BadSnapshotURL("Check 'https://coinmarketcap.com/historical/' "
                                 "for available historical snapshot periods ")
        else:
            snap_df = pd.read_html(snap_url)[0]

        cleaned_df = snap_df.rename({"#": "Rank"}, axis=1)
        cleaned_df = cleaned_df.iloc[0:, :-1]
        return cleaned_df

    @classmethod
    def from_strings(cls, string_period, hyphen=True):
        """
        An alternative constructor for retrieving historical snapshots of crypto-currency markets via CoinMarketCap.

        :param string_period: str object specifying the period under consideration.
        :param hyphen: bool value with the default value
                       indicating a separation of string_period by a "-" and "/" otherwise.

        :return: A Pandas DataFrame object with historical snapshot data of the period specified.
        """
        if hyphen:
            string_period = datetime.strptime(string_period, "%Y-%m-%d").date()
        else:
            string_period = datetime.strptime(string_period, "%Y/%m/%d").date()
        return cls(string_period).get_snapshot()


# Current class for all methods related to current crypto-currency information
class Current:
    """
    A class that connects to CoinMarketCap API and returns current
    data information for specified ticker.
    """
    pass
