import unittest
import warnings
from datetime import date
from coinsta.exceptions import WrongCoinCode, BadSnapshotURL
from coinsta.core import Historical, Current, HistoricalSnapshot


class TestCoinsta(unittest.TestCase):

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
        warnings.filterwarnings("ignore", message="can't resolve package from __spec__ or __package__, "
                                                  "falling back on __name__ and __path__")

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
        btc_current = Current.get_current('btc')
        no_items = len(btc_current.index)
        self.assertEqual(no_items, 12)

    def test_bad_current(self):
        with self.assertRaises(AttributeError):
            return Current.get_current('kkk')

    def test_global_info(self):
        glo_info = Current.global_info()
        no_keys = len(glo_info.keys())
        self.assertEqual(no_keys, 5)

    def test_top_100(self):
        top_100 = Current.top_100()
        no_cols = len(top_100.columns)
        self.assertEqual(no_cols, 9)

    def test_historical_snapshot(self):
        snap_date = date(2018, 7, 29)
        july_2018 = HistoricalSnapshot(snap_date)
        july_2018_snapshot = july_2018.get_snapshot()
        len_july_2018 = len(july_2018_snapshot.columns)
        self.assertEqual(len_july_2018, 10)

    def test_snapshot_period(self):
        with self.assertRaises(BadSnapshotURL):
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
