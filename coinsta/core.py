# needed libraries
from datetime import date, datetime
import pandas as pd
import requests
from coinsta.exceptions import WrongCoinCode, CoinMarketCapDown, BadSnapshotURL


# Historical Class for all methods related to historical data
class Historical:
    """
    A class that provides methods for scraping historical price data
    based on specified cryptocurrencies and time period from
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

        # check for mispecification
        if isinstance(start, date) is False:
            raise TypeError("Start argument must be a date object or strings with the alternative 'from_strings' "
                            "constructor")

        # convert start day into to appriopriate format for scraping data from CoinMarketCap
        start = start.isoformat().replace("-", "")

        # use today's date unless otherwise specified by user
        if end is None:
            today = date.today()
            formatted_today = today.isoformat().replace("-", "")
            end = formatted_today
        elif isinstance(end, date) is False:
            raise TypeError("End argument must be a date object or \
                                        strings with the alternative 'from_strings' constructor")
        else:
            end = end.isoformat().replace("-", "")

        # self assign default args 
        self.ticker = ticker
        self.start = start
        self.end = end

    def __repr__(self):
        return "<Historical({0}, {1}, {2})>".format(self.ticker, self.start, self.end)

    def __str__(self):

        def readable_date(string):
            return datetime.strptime(string, '%Y%m%d').date().strftime('%B %d, %Y')

        return "Coinsta object: \n crypto_symbol: {0} \n start_period: {1} \n" \
               " end_period: {2}".format(self.ticker,
                                         readable_date(self.start),
                                         readable_date(self.end)
                                         )

    def get_data(self):
        """
        This function scrapes and cleans the data of the specified tickers
        from CoinMarketCap website.

        :return: A Pandas DataFrame object containing historical data on the specified tickers.
        """
        def ticker_checker(ticker):
            """
            This method shows all valid coin tickers used by
            the CoinMarketCap website. Users can use this method
            to know the name of the cryptocurrency of interest.
            """
            api_url = "https://api.coinmarketcap.com/v2/ticker/?limit=0"
            api_check = requests.get(api_url)

            if api_check.status_code != 200:
                raise CoinMarketCapDown("CoinMarketCap API is down. Try later")
            else:
                response = requests.get(api_url).json()

            coins_dict = response['data']

            for v in coins_dict.values():
                if v['symbol'] == ticker.upper():
                    return v['website_slug']
            raise WrongCoinCode('Invalid code from "coinmarketcap.com"')

        slug = ticker_checker(self.ticker)

        site_url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(slug,
                                                                                                        self.start,
                                                                                                        self.end)

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


# Current class for all methods related to current cryptocurrency information
class Current:
    """
    A class that connects to CoinMarketCap API and returns current
    data information for specified ticker.
    """

    def __init__(self):
        # check for API read errors
        api_link = "https://api.coinmarketcap.com/v2/ticker/?limit=0"
        api_check = requests.get(api_link)
        if api_check.status_code != 200:
            raise CoinMarketCapDown("CoinMarketCap API is down. Try later")
        else:
            pass

    @staticmethod
    def get_current(ticker):
        """
        This method returns the current information on tickers supplied.

        :param ticker: a str object representing the ticker information of the cryptocurrency under consideration.
        :return: A Pandas DataFrame object with current data on the specified ticker.
        """
        def get_info():
            url = "https://api.coinmarketcap.com/v2/ticker/?limit=0"
            response = requests.get(url).json()

            coins_dict = response['data']

            for v in coins_dict.values():
                if v['symbol'] == ticker.upper():
                    my_dict = dict()
                    my_dict['name'] = v['name']
                    my_dict['symbol'] = v['symbol']
                    my_dict['rank'] = v['rank']
                    my_dict['circulating_supply'] = v['circulating_supply']
                    my_dict['total_supply'] = v['total_supply']
                    my_dict['max_supply'] = v['max_supply']

                    quotes = v['quotes']['USD']

                    for key, val in quotes.items():
                        my_dict[key] = val

                    return my_dict

            else:
                WrongCoinCode('Invalid code from "coinmarketcap.com"')

        info = get_info()

        return pd.DataFrame.from_dict(info, orient='index', columns=[info.get('name')])

    @staticmethod
    def global_info():
        """
        This method returns a dictionary on global information
        representing the status of all cryptocurrencies
        tracked by Coinmarketcap.

        :return: A dictionary object with data on global cryptocurrency markets.
        """
        global_url = 'https://api.coinmarketcap.com/v2/global/'
        global_response = requests.get(global_url).json()

        for _, _ in global_response.items():
            glo_dict = dict()

            glo_dict['active_cryptos'] = global_response['data']['active_cryptocurrencies']
            glo_dict['active_markets'] = global_response['data']['active_markets']
            glo_dict['btc_dominance'] = global_response['data']['bitcoin_percentage_of_market_cap']

            glo_quotes = global_response['data']['quotes']['USD']

            for key, value in glo_quotes.items():
                glo_dict[key] = value

            return glo_dict  # pd.DataFrame.from_dict(glo_dict, orient='index')

    @staticmethod
    def top_100():
        """
        This method returns the name, ticker symbol and current price
        of the top 100 cryptocurrencies in terms of market capitalisation.

        :return: A Pandas DataFrame object with data on the top 100 cryptocurrencies.
        """
        api_url = "https://api.coinmarketcap.com/v2/ticker/?limit=0"

        check_response = requests.get(api_url)

        if check_response.status_code == 200:

            top_response = requests.get(api_url).json()

            results_dict = {}

            for _, v in top_response['data'].items():

                container = dict()

                container['name'] = v['name']
                container['symbol'] = v['symbol']
                container['rank'] = v['rank']

                deep_nest = v['quotes']['USD']

                for key, value, in deep_nest.items():
                    container[key] = value

                results_dict[container['name']] = container

            df = pd.DataFrame.from_dict(results_dict, orient='index').reset_index(drop=True)

            return df.sort_values('rank').reset_index(drop=True)
        else:
            raise CoinMarketCapDown("CoinMarketCap API is down. Try later")


# A class that handles historical snapshots of crypto markets
class HistoricalSnapshot:
    """
    A class that returns a historical snapshot of Cryptocurrency market information
    on a specified period of time.
    """

    def __init__(self, period):
        assert isinstance(period, date)
        self.period = period

    def __repr__(self):
        return "<HistoricalSnapshot({0})>".format(self.period)

    def __str__(self):
        def readable_date(specified_date):
            return specified_date.strftime('%B %d, %Y')

        return "CoinMarketCap Historical Snapshot for the period: {0}".format(readable_date(self.period))

    def get_snapshot(self):
        """
        A method the retrieves a historical snapshot of cryptocurrency markets via CoinMarketCap.

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
        An alternative constructor for retrieving historical snapshots of cryptocurrency markets via CoinMarketCap.

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


