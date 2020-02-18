import requests
import json
from datetime import datetime
import pandas as pd
from coinsta.exceptions import WrongCoinCode
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def _readable_date(string):
    """
    A function that accepts a string formatted date and return a more readable data string format.

    :param string: string formatted date
    :return: Human readable string formatted date
    """
    return datetime.strptime(string, '%Y%m%d').date().strftime('%B %d, %Y')


def _snapshot_readable_date(specified_date):
    """
    A function that transforms the specified date into a more human friendly string formatted date

    :param specified_date: string formatted date
    :return: Human readable string formatted date
    """
    return specified_date.strftime('%B %d, %Y')


def _ticker_checker(ticker):
    """
    A function that verifies and returns the right website id based on the supplied crypto ticker.

    :param ticker: crypto ticker as a string
    :return: A string object representing the website crypto id for the supplied ticker
    """
    try:
        # Pass the html from CoinMarketCap to Pandas
        url = "https://coinmarketcap.com/all/views/all/"
        df = pd.read_html(url)[-1]

        # Get a dictionary of the names and symbols
        check_dict = df[['Name', 'Symbol']].to_dict('records')

        # Upper case user supplied ticker
        ticker = ticker.upper()

        for item in check_dict:
            # Return the site id for the user specified  ticker
            if item['Symbol'] == ticker:
                return item['Name']

        raise WrongCoinCode("'{0}' is unavailable on CoinMarketCap.com. Please check the website for the "
                            "right ticker information code".format(ticker))
    except Exception as e:
        raise e


def _parse_cmc_url(url, api_key, **kwargs):
    """
    This function takes the user supplied url link and API key along with acceptable parameters to
    CoinMarketCap PRO API and returns the JSON response data.

    :param url: HTTP link to an acceptable CoinMarketCap API endpoint
    :param api_key: API key from CoinMarketCap in strings
    :param kwargs: All acceptable parameters available in CoinMarketCap API
    :return: JSON object containing response data
    """

    parameters = {
        key: val for key, val in kwargs.items()
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key

    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        response_json = json.loads(response.text)
        session.close()
        return response_json

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise e
