import requests
import json
from datetime import datetime
from pyquery import PyQuery
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
        # Pass the html from CoinMarketCap to PyQuery
        url = "https://coinmarketcap.com/all/views/all/"
        html = requests.get(url).text
        raw_html = PyQuery(html)

        # Upper case user supplied ticker
        ticker = ticker.upper()

        # Locate all table rows in the raw html ignoring the table header row
        rows = raw_html('tr')[1:]

        # Go through each row selecting the ticker and the associated id used by CoinMarketCap url
        for row in rows:
            crypto_ticker = row.cssselect("td.text-left.col-symbol")[0].text_content()  # ticker
            website_crypto_id = row.values()[0].split("id-")[1]  # CoinMarketCap site id for ticker

            # Return the site id for the user specified  ticker
            if ticker == crypto_ticker:
                return website_crypto_id
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
