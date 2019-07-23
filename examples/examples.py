import sys
sys.path.insert(0, '')
from datetime import date
from coinsta.core import Historical, Current, HistoricalSnapshot


cur = Current(api_key='YOUR-API-KEY-HERE', currency='eur')  # Default is usd
print(cur)

# specify dates considered
start = date(2018, 3, 1)
end = date(2018, 6, 1)

# get data
coin_spec = Historical('btc', start=start, end=end)
btc_data = coin_spec.get_data()
print(btc_data.head())

# default alternative method for "-" formatted date strings
alt_spec = Historical.from_strings('btc', '2018-3-1','2018-6-1', hyphen=True)

alt_btc = alt_spec.get_data()
print(alt_btc.head())

# another alternative method for "/" formatted date strings
other_spec = Historical.from_strings('btc', '2018/3/1','2018/6/1', hyphen=False)

another_btc = other_spec.get_data()
print(another_btc.head())


# get current market information on a specified crypto
btc_current = cur.get_current('btc')
print(btc_current)

# get the top 100 cryptos (in terms of market cap)
current_100 = cur.top_100()
print(current_100.head())

# get global overview of crypto markets
glo_info = cur.global_info()
print(glo_info)

# Historical Snapshot
snap_period = date(2013, 4, 28)
early_2013 = HistoricalSnapshot(snap_period).get_snapshot()
print(early_2013.info())

early_2013 = HistoricalSnapshot.from_strings('2013/4/28', hyphen=False)
print(early_2013.info())


early_2013 = HistoricalSnapshot.from_strings('2013-4-28')
print(early_2013.info())

print(Historical(ticker='btc', start=date(2016, 1, 2)))

snap_date = date(2018, 7, 29)
july_2018 = HistoricalSnapshot(snap_date)
july_2018_snapshot = july_2018.get_snapshot()
print(july_2018_snapshot.info())

fake_date = date(1999, 1, 1)
fake_data = HistoricalSnapshot(fake_date).get_snapshot()
print(fake_data.info())

july_2018 = HistoricalSnapshot.from_strings('2018-7-29')
print(len(july_2018.columns))


