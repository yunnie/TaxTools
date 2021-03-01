import unittest
import src.taxtools as Tools
import pandas as pd
from functools import reduce
import os

class TestDatasetFunctions(unittest.TestCase):

    def test_date_filter(self):
        data = pd.read_pickle("tests/data/tiingo_sample.pkl")
        subset = Tools.subsetByYear(data, 2020)
        self.assertTrue(subset.shape[0] > 250)
        self.assertTrue(subset.shape[0] < data.size)
        dates = list(map(lambda row: row[1], subset.index.values))
        self.assertTrue(
            reduce(
                lambda isTrue, timestamp: timestamp.year == 2020 and
                isTrue, dates, True)
        )

    def test_find_last_date(self):
        data = pd.read_pickle("tests/data/tiingo_sample.pkl")
        temp = Tools.subsetByYear(data, 2020)
        last = Tools.findLastDay(temp)
        self.assertTrue(last.shape[0] == 1)
        self.assertTrue(last.index.values[0][1].month == 12)

    def test_find_max_close(self):
        data = pd.read_pickle("tests/data/tiingo_sample.pkl")
        close = data.close.tolist()
        maxValue = reduce(lambda a, b: max(a,b), close)
        maxRow = Tools.findMaxClose(data)
        self.assertEqual(maxRow, maxValue)

    def test_sum_dividends(self):
        data = pd.read_pickle("tests/data/tiingo_sample.pkl")
        data['divCash'] = 1.0
        dividends = Tools.findTotalDividends(data)
        self.assertEqual(dividends, len(data))

    def test_read_asset_list(self):
        assets = Tools.readAssetList("tests/data/testAssetList.csv")
        self.assertEqual(assets.columns.tolist(),
            ['Account', 'Symbol', 'Name', 'Qty',
             'MaxValue', 'LastValue', 'Dividends'])

    def test_process_asset_list(self):
        assets = Tools.readAssetList("tests/data/testAssetList.csv")
        finished = Tools.processAssetList(assets, 2020)
        self.assertEqual(len(finished), 2)
