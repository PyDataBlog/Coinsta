import unittest
from datetime import date
from coinsta.exceptions import WrongCoinCode, BadSnapshotURL
from coinsta.core import Historical, Current, HistoricalSnapshot


class TestCoinsta(unittest.TestCase):
    k = '0f73d522-ffa1-4b41-8339-95a6702b74d1'
    def test_historical(self):

        with self.assertRaises(TypeError):
            start = date(2018, 2, 20)
            return Historical('dash', start=start, end=123)

    def test_historical_start(self):

        with self.assertRaises(TypeError):
            end = date(2018, 2, 20)
            return Historical('dash', start=123, end=end)

    def test_historical_ticker(self):

        with self.assertRaises(WrongCoinCode):
            start = date(2018, 2, 20)
            return Historical('fake_ticker', start=start).get_data()

    def test_get_data(self):
        coin_spec = Historical.from_strings('dash', '2018-1-1', '2018-3-1', hyphen=True)
        data = coin_spec.get_data()
        data_cols = len(data.columns)

        self.assertEqual(data_cols, 6)

    def test_from_strings(self):
        alt_spec = Historical.from_strings('xrp', '2018-1-1', '2018-3-1', hyphen=True)
        start = alt_spec.start
        end = alt_spec.end
        ticker = alt_spec.ticker

        self.assertEqual(start, '20180101')
        self.assertEqual(end, '20180301')
        self.assertEqual(ticker, 'xrp')

    def test_from_strings_2(self):
        alt_spec = Historical.from_strings('btc', '2018/1/1', '2018/3/1', hyphen=False)
        start = alt_spec.start
        end = alt_spec.end
        ticker = alt_spec.ticker

        self.assertEqual(start, '20180101')
        self.assertEqual(end, '20180301')
        self.assertEqual(ticker, 'btc')

    def test_get_current(self):
        cur = Current(TestCoinsta.k)
        cur_btc = cur.get_current('btc')
        size = len(cur_btc.keys())
        self.assertEqual(size, 13)


    def test_global_info(self):
        cur = Current(TestCoinsta.k)
        global_100 = cur.global_info()
        size = len(global_100)

        self.assertEqual(size, 10)

    def test_top_100(self):
        cur = Current(TestCoinsta.k, currency='usd')
        top_100 = cur.top_100()
        size_cols = len(top_100.columns)

        self.assertEqual(size_cols, 20)

    def test_historical_snapshot(self):
        snap_date = date(2018, 7, 29)
        july_2018 = HistoricalSnapshot(snap_date)
        july_2018_snapshot = july_2018.get_snapshot()
        len_july_2018 = len(july_2018_snapshot.columns)
        self.assertEqual(len_july_2018, 11)

    def test_snapshot_period(self):
        with self.assertRaises(ValueError):  # replace with BadSnapshotURL
            fake_date = date(1999, 1, 1)
            return HistoricalSnapshot(fake_date).get_snapshot()

    def test_snapshot_strings(self):
        july_2018 = HistoricalSnapshot.from_strings('2018-7-29')
        len_july_2018 = len(july_2018.columns)
        self.assertEqual(len_july_2018, 10)

    def test_snapshot_strings2(self):
        july_2018 = HistoricalSnapshot.from_strings('2018/7/29', hyphen=False)
        len_july_2018 = len(july_2018.columns)
        self.assertEqual(len_july_2018, 10)


if __name__ == '__main__':
    unittest.main()
