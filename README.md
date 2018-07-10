# Coinsta
A Python :snake: package for acquiring both historical and current data of cryptocurrencies:moneybag:.
___

**Author:** Bernard Brenyah
#### Project Status
[![Latest Version](https://pypip.in/version/coinsta/badge.svg)](https://pypi.python.org/pypi/coinsta/)
[![Build Status](https://www.travis-ci.org/PyDataBlog/Coinsta.svg?branch=master)](https://www.travis-ci.org/PyDataBlog/Coinsta)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta?ref=badge_shield)
[![License](https://pypip.in/license/coinsta/badge.svg)](https://pypi.python.org/pypi/coinsta/)
[![Supported Python Version](https://pypip.in/py_versions/coinsta/badge.svg)](https://pypi.python.org/pypi/coinsta/)
[![HitCount](http://hits.dwyl.io/PyDataBlog/Coinsta.svg)](http://hits.dwyl.io/PyDataBlog/Coinsta)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/PyDataBlog/Coinsta/master)

## Table of Content
1. [Motivation](#motivation) 
2. [Frameworks Used](#frameworks-used)
3. [Installation](#installation)
4. [Features](#features)
    - 4.1 [Pending Features](#pending-features)
5. [How To Use](#how-to-use)
6. [Release History](#release-history)
7. [How To Contribute](#how-to-contribute)
8. [Credits](#credits)
9. [License](#license)
___
### Motivation
Why `coinsta`?
I spent the past couple of months on a graduate dissertation which required the use of both historical and current data on cryptocurrencies. After browsing the Python Packaging Index (PYPI), I was frustrated by the lack of a Python package that catered for such needs. As far as I know only [cyrptoCMD](https://github.com/guptarohit/cryptoCMD) came close to meeting my needs. The only drawback is the that package only delivers historical data. OK so "*why not edit that project and make a pull request with your suggestions?*"

That was the original plan until I realised that the scraping code could relatively be done quickly with the help of `pandas` package. If I went with the original plan I would have to rewrite the whole code and implementation ideas for `cryptoCMD` project. The only logical conclusion was starting a new project that I wish I had during my data collection process. A project inspired by scripts I generated for my dissertation project.

As a result, this project is the first Python project that supplies both historical and current data on cryptocurrency markets and assets in one coherent package.
____

### Frameworks Used
This package leverages the power of the following packages:
- `pandas`
- `requests`
- `lxml`
___
### Installation
The easiest way to install Coinsta is to use the default python package installer `pip`:

```
pip install coinsta
```

and for the few brave ones who like bleeding edge technology, the latest source can be installed via with this command:

```
pip install git+git://github.com/PyDataBlog/Coinsta.git
```
___
### Features
- Current global information on cryptocurrency markets
- Current market information on the top 100 cryptocurrencies
- Current data on a specified cryptocurrency 
- Historical data on all active cryptocurrencies

##### Pending Features
- [X] Support for Python 3.5
- [ ] Miscellaneous Functions
- [ ] Contribution guidelines
- [X] test compliance with Python 3.7
- [ ] Improve documentation and doc strings
- [ ] Optimizaton of code
- [ ] Support for CoinMarketCap's historical snapshots
- [ ] Support for market index comparisons

### How To Use
**Historical Data:**
```py
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

'''
by default the end date is set to use the "today's" date
 of the user unless otherwise specified like above
'''
```
**Alternative Constructors for Historical data from dates in the form of strings (YYYY-MM-DD) or (YYYY/MM/DD):**

```py
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

```
    Open     High      Low    Close      Volume    Market_cap
Date
```
**Current Data:**
```py
# import the Current class 
from coinsta.core import Current

# get current market information on a specified crypto
btc_current = Current.get_current('btc')
print(btc_current)

# get the top 100 cryptos (in terms of market cap)
current_100 = Current.top_100()
print(current_100.head())

# get global overview of crypto markets
glo_info = Current.global_info()
print(glo_info)


```
The `get_current()` method from the current class returns a `pandas` DataFrame object with one column representing the following named rows of information on the cryptocurrency specified:

```
name                    
symbol               
rank                 
circulating_supply 
total_supply        
max_supply              
price                   
volume_24h          
market_cap          
percent_change_1h          
percent_change_24h         
percent_change_7d    
```
The `top_100` method in the current class returns a `pandas` DataFrame object of the top 100 cryptocurrencies in terms of market capitalization. The following are the columns returned:

```
['name', 'symbol', 'rank', 'price', 'volume_24h', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d']
```

Finally, the `global_info()` method in Current class returns a dictionary with the following keys as an overview of cryptocurrency markets as a whole

```
dict_keys(['active_cryptos', 'active_markets', 'btc_dominance', 'total_market_cap', 'total_volume_24h'])
```
___
### Release History
- 0.1.2  - Added support for Python 3.5 and 3.7 
- 0.1.1  - Added license info and improved documentation 
- 0.1.0  - Initial Public Release

### How to Contribute
This project welcomes contributions from anyone interested in this project. Guidelines for contribution is being drafted but for now a pull request with explanation of the contributions will suffice.
___
### Credits
Shoutout to [CoinMarketCap]() :heart: for the access to their API as well as allowing projects such as this plug into the datawarehouse.
___
### License
License: [BSD-3](https://github.com/PyDataBlog/Coinsta/blob/master/LICENSE) 

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyDataBlog%2FCoinsta?ref=badge_large)
___
[Back to top](#table-of-content)