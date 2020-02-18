# Needed libraries
import pandas as pd
from pandas import json_normalize
from coinsta.exceptions import BadSnapshotURL, WrongCoinCode, ApiKeyError
from coinsta.utils import _readable_date, _ticker_checker, _snapshot_readable_date, _parse_cmc_url
from datetime import date, datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


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
        df = data[-1]

        # Clean up the DataFrame
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

        try:
            snap_df = pd.read_html(snap_url)  # Check for the existence of the table
        except ValueError:
            raise BadSnapshotURL("Check 'https://coinmarketcap.com/historical/' "
                                 "for available historical snapshot periods ")

        snap_df = pd.read_html(snap_url)[-1]

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

    Supported fiat currencies: 'https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions'
    API Keys signup available at: 'https://pro.coinmarketcap.com/signup/'
    """

    def __init__(self, api_key=None, currency='USD'):
        self.api_key = api_key
        self.currency = currency.upper()

    def __repr__(self):
        return "<Current(api_key={0}, currency{1})>".format(self.api_key, self.currency)

    def __str__(self):
        return "Current class specified with key: {0} & currency: {1}".format(self.api_key, self.currency)

    def get_current(self, ticker):
        """
        The method returns the latest price information for the user supplied ticker.

        :param ticker: A string representing the ticker of the crypto-currency of interest.
        :return: A dictionary object containing current market and price information on the ticker supplied.
        """
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

        try:
            response_data = _parse_cmc_url(url=url, api_key=self.api_key, convert=self.currency, symbol=ticker.upper())

            if response_data['status']['error_code'] == 400:
                raise WrongCoinCode('Invalid ticker from "CoinMarketCap.com". Please supply a valid crypto ticker')

            elif response_data['status']['error_code'] == 401:
                raise ApiKeyError('Please check API Key as it was rejected by CoinMarketCap')

            else:
                coins_dict = response_data['data']

                for v in coins_dict.values():

                    my_dict = dict()
                    my_dict['name'] = v['name']
                    my_dict['symbol'] = v['symbol']
                    my_dict['rank'] = v['cmc_rank']
                    my_dict['circulating_supply'] = v['circulating_supply']
                    my_dict['total_supply'] = v['total_supply']
                    my_dict['max_supply'] = v['max_supply']

                    quotes = v['quote'][self.currency]

                    for key, val in quotes.items():
                        my_dict[key] = val

                    return my_dict

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise e

    def global_info(self):
        """
        A method that returns market information at the global level.

        :return: A dictionary object containing global market information of crypto-currencies.
        """
        url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

        try:
            global_response = _parse_cmc_url(url=url, api_key=self.api_key, convert=self.currency)

            for _, _ in global_response.items():

                glo_dict = dict()

                glo_dict['active_cryptos'] = global_response['data']['active_cryptocurrencies']
                glo_dict['active_exchanges'] = global_response['data']['active_exchanges']
                glo_dict['btc_dominance'] = global_response['data']['btc_dominance']
                glo_dict['eth_dominance'] = global_response['data']['eth_dominance']

                glo_quotes = global_response['data']['quote'][self.currency]

                for key, value in glo_quotes.items():
                    glo_dict[key] = value

                return glo_dict  # pd.DataFrame.from_dict(glo_dict, orient='index')

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise e

    def top_100(self, limit=100):
        """
        A method that

        :param limit: Integer (default=100) representing the number of listings
        :return: A Pandas DataFrame object containing all market and price information of number of listings requested
        """

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        try:
            top_response = _parse_cmc_url(url=url, api_key=self.api_key, convert=self.currency, limit=limit)

            # Convert the data from the json into a Pandas DataFrame
            df = pd.DataFrame.from_records(top_response['data'])

            #
            main_df = df.drop('quote', axis='columns')
            expanded_df = json_normalize(df['quote'])

            combo_df = pd.concat([main_df, expanded_df], axis='columns')
            return combo_df

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise e
