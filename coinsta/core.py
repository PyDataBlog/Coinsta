# needed libraries
from datetime import date, datetime
import pandas as pd
import requests
from coinsta.exceptions import WrongCoinCode

'''
        TODO
        - make logo
        - submit to zenodo
        - clean up setup code
'''


# Historical Class for all methods related to historical data
class Historical:
    """
    A  class that provides methods for scraping historical price data
    based on specified cryptocurrencies and time period from
    CoinMarketCap.
    """

    def __init__(self, ticker, start, end=None):
        """
        :start argument accepts a date object representing YYYYMMDD.
        :end argument accepts a date object representing YYYYMMDD.
        :ticker argument accepts strings representing ticker information
        """

        # check for mispecification
        if isinstance(start, date) is False:
            raise TypeError("Start argument must be a date object or strings with the alternative 'from_strings' "
                            "constructor")

        # convert start day into to appriopriate format
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
        return "Coinsta object: \n crypto_symbol: {0} \n start_period: {1} \n end_period: {2}".format(self.ticker,
                                                                                                      self.start,
                                                                                                      self.end)

        # f"Coinsta object: \n crypto_symbol: {self.ticker}" \
        # f"\n start_period: {self.start} \n end_period: {self.end}\n"

    def get_data(self):
        """
        This function scrapes and cleans the data of the specified tickers
        from CoinMarketCap website.
        """

        def ticker_checker(ticker):
            """
            This method shows all valid coin tickers used by
            the CoinMarketCap website. Users can use this method
            to know the name of the cryptocurrency of interest.
            """

            api_url = "https://api.coinmarketcap.com/v2/ticker/?limit=0"
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
        # f"https://coinmarketcap.com/currencies/{slug}/historical-data/?start={self.start}&end={self.end}"

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
        Default format is the hyphen separate string: YYYY-MM-DD
        Turn arg `hyphen` to False if string to be parsed is: YYYY/MM/DD
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
    data information for specified ticker
    """

    def __init__(self):
        # check for the required presence of pandas package
        # replace with check for API read errors instead
        try:
            import pandas as pd
        except ImportError:
            pd = None

        if pd is None:
            raise NotImplementedError(
                "This package requires the installation of the 'pandas' package"
                "Install 'pandas' package with pip or conda"
            )
        else:
            pass

    @staticmethod
    def get_current(ticker):
        """
        A method the returns the current data on specified cryptocurrency tickers
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
        of the top 100 cryptocurrencies in terms of market capitalisation
        """
        api_url = "https://api.coinmarketcap.com/v2/ticker/?limit=0"
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


'''
class HistoricalSnapshot:
    """
    A class that returns a historical snapshot of Cryptocurrency market with information
    on the highest ranking cryptocurrencies.
    """
    pass

'''
