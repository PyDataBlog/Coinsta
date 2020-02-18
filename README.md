# Coinsta

A Python :snake: package for acquiring both historical and current data of crypto-currencies:moneybag:.
_________________________________________________________________________________________________________

**Author:** Bernard Brenyah

## Project Status

[![Latest Version](https://img.shields.io/pypi/v/coinsta.svg)](https://pypi.python.org/pypi/coinsta/)
[![Build Status](https://www.travis-ci.org/PyDataBlog/Coinsta.svg?branch=master)](https://www.travis-ci.org/PyDataBlog/Coinsta)
[![Issues](https://img.shields.io/github/issues/PyDataBlog/coinsta.svg)](https://github.com/PyDataBlog/Coinsta/issues)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/PyDataBlog/Coinsta/commits/master)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta?ref=badge_shield)
[![License](https://img.shields.io/pypi/l/coinsta.svg?color=green)](https://pypi.python.org/pypi/coinsta/)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/coinsta.svg)](https://pypi.python.org/pypi/coinsta/)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/PyDataBlog/Coinsta/master)

## Table of Content

1. [Motivation](#motivation)
2. [Frameworks Used](#frameworks-used)
3. [Installation](#installation)
4. [Features](#features)
5. [Pending Features](#pending-features)
6. [How To Use](#how-to-use)
7. [Release History](#release-history)
8. [How To Contribute](#how-to-contribute)
9. [Credits](#credits)
10. [License](#license)

_________________________________________________________________________________________________________

### Motivation

Why `coinsta`?
I spent the past couple of months on a graduate dissertation which required the use of both historical and current data on cryptocurrencies. After browsing the Python Packaging Index (PYPI), I was frustrated by the lack of a Python package that catered for such needs. As far as I know only [cyrptoCMD](https://github.com/guptarohit/cryptoCMD) came close to meeting my needs. The only drawback is the that package only delivers historical data. OK so "*why not edit that project and make a pull request with your suggestions?*"

That was the original plan until I realised that the scraping code could relatively be done quickly with the help of `pandas` package. If I went with the original plan I would have to rewrite the whole code and implementation ideas for `cryptoCMD` project. The only logical conclusion was starting a new project that I wish I had during my data collection process. A project inspired by scripts I generated for my dissertation project.

As a result, this project is the first Python project that supplies both historical and current data on cryptocurrency markets and assets in one coherent package.

_________________________________________________________________________________________________________

### Frameworks Used

This package leverages the power of the following packages:

- `pandas`
- `requests`
- `lxml`
- `beautifoulsoup`

_________________________________________________________________________________________________________

### Installation

The easiest way to install Coinsta is to use the default python package installer `pip`:

```bash
pip install coinsta
```

and for the few brave ones who like bleeding edge technology, the latest source can be installed via with this command:

```bash
pip install git+git://github.com/PyDataBlog/Coinsta.git
```

_________________________________________________________________________________________________________

### Features

- Current global information on cryptocurrency markets.
- Current market information on the top 100 cryptocurrencies.
- Current data on a specified cryptocurrency.
- Historical data on all active cryptocurrencies.
- Get historical snapshots of cryptocurrencies.

### Pending Features

- [X] Migrate the current class to the new CoinMarketCap API.
- [X] Dropped support for Python 3.5.
- [X] Added support for Python 3.8.
- [X] Improve documentation and doc strings.
- [X] Optimisation of code.
- [X] Support for CoinMarketCap's historical snapshots.

#### How To Use

**Historical Data**

```python
# import the Historical class
from coinsta.core import Historical
from datetime import date

# specify dates considered
start = date(2018, 3, 1)
end = date(2018, 6,1)

# get data
coin_spec = Historical('btc', start=start, end=end)
btc_data = coin_spec.get_data()
print(btc_data.head())


#by default the end date is set to use the "today's" date
# of the user unless otherwise specified like above

```

**Alternative Constructors for Historical data from dates in the form of strings (YYYY-MM-DD) or (YYYY/MM/DD):**

```python
from coinsta.core import Historical

# default alternative method for "-" formatted date strings
alt_spec = Historical.from_strings('btc', '2018-3-1','2018-6-1', hyphen=True)

alt_btc = alt_spec.get_data()
print(alt_btc.head())

# another alternative method for "/" formated date strings
other_spec = Historical.from_strings('btc', '2018/3/1','2018/6/1', hyphen=False)

another_btc = other_spec.get_data()
print(another_btc.head())

```

The `get_data()` method and the `from_strings` method from the Historical class returns a `pandas` DataFrame object with sorted in an ascending order indexed the dates specified by the user:

```shell
    Open     High      Low    Close      Volume    Market_cap
Date
```

So what was the top cryptocurrency (in terms of market capitalisation) on date XYZ?
Luckily, CoinMarketCap delivers periodic snapshots of the this type of rankings. The `HistoricalSnapshot` class taps into data to supply users with such information.

The Historical Snapshot feature returns a Pandas DataFrame object with the following self describing columns:

```python
Index(['Rank', 'Name', 'Symbol', 'Market Cap', 'Price', 'Circulating Supply',
       'Volume (24h)', '% 1h', '% 24h', '% 7d'],
      dtype='object')
```

**Historical Snapshots:**

```python
from coinsta.core import HistoricalSnapshot
from datetime import date

snap_date = date(2018, 7, 29)

july_2018 = HistoricalSnapshot(snap_date)
july_2018_snapshot = july_2018.get_snapshot()

print(july_2018_snapshot.info())
```

**Current Data:**

```python
# import the Current class and instantiate the current class object with specifications
from coinsta.core import Current
cur = Current(api_key='YOUR-API-KEY-HERE', currency='eur')  # Default is usd

# get current market information on a specified crypto
btc_current = cur.get_current('btc')
print(btc_current)

# get the top 100 cryptos (in terms of market cap)
current_100 = cur.top_100(limit=100)  # Default limit is 100 but can be increased as a user wishes
print(current_100.head())

# get global overview of crypto markets
glo_info = cur.global_info()
print(glo_info)


```

The `get_current()` method from the current class returns a `pandas` DataFrame object with one column representing the following named rows of information on the cryptocurrency specified:

```python
dict_keys(['name', 'symbol', 'rank', 'circulating_supply',
 'total_supply', 'max_supply', 'price', 'volume_24h',
  'percent_change_1h', 'percent_change_24h', 'percent_change_7d',
   'market_cap', 'last_updated'])
```

The `top_100` method in the current class returns a `pandas` DataFrame object of the top 100 cryptocurrencies in terms of market capitalization. The following are the columns returned:

```python
['id', 'name', 'symbol', 'slug', 'num_market_pairs', 'date_added',
 'tags', 'max_supply', 'circulating_supply', 'total_supply', 'platform',
 'cmc_rank', 'last_updated', '*currency*.price', '*currency*.volume_24h',
 '*currency*.percent_change_1h', '*currency*.percent_change_24h', '*currency*.percent_change_7d',
  '*currency*.market_cap', '*currency*.last_updated']
```

Finally, the `global_info()` method in Current class returns a dictionary with the following keys as an overview of cryptocurrency markets as a whole

```python
dict_keys(['active_cryptos', 'active_exchanges', 'btc_dominance',
 'eth_dominance', 'total_market_cap', 'total_volume_24h',
 'total_volume_24h_reported', 'altcoin_volume_24h',
 'altcoin_volume_24h_reported', 'altcoin_market_cap', 'last_updated'])
```

_________________________________________________________________________________________________________

#### Release History
- 0.1.7 - Trimmed code dependencies.
- 0.1.6 - Fix compliance with upstream changes, added support for Python 3.8 and dropped support for Python 3.5.
- 0.1.5 - Updated historical snapshot to suit the new upstream changes from CoinMarketCap
- 0.1.4 - Re-wrote the Current classes to use the new CoinMarketCap API
- 0.1.3  - Added Historical Snapshot feature
- 0.1.2  - Added support for Python 3.5 and 3.7
- 0.1.1  - Added license info and improved documentation
- 0.1.0  - Initial Public Release

#### How to Contribute

This project welcomes contributions from anyone interested in this project. Guidelines for contribution is being drafted but for now a pull request with explanation of the contributions will suffice.

_________________________________________________________________________________________________________

#### Credits

Shoutout to [CoinMarketCap](https://coinmarketcap.com/) :heart: for the access to their API as well as allowing projects such as this plug into the datawarehouse.

_________________________________________________________________________________________________________

#### License

License: [BSD-3](https://github.com/PyDataBlog/Coinsta/blob/master/LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta?ref=badge_large)

_________________________________________________________________________________________________________

[Back to top](#table-of-content)
