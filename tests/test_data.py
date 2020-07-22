import unittest
from datetime import date
from jugaad_data import NSEHistory

class TestNSEHistory(unittest.TestCase):
    h = NSEHistory()
    h.base_url = "https://23.54.86.108"    
    h.ssl_verify = False

    def test_symbol_count(self):
        sym_count = self.h._symbol_count("SBIN")
        self.assertEqual(sym_count, '1')
        sym_count = self.h._symbol_count("RELIANCE")
        self.assertEqual(sym_count, '2')


    def test__stock_history(self):
        symbol = "RELIANCE"
        from_date = date(2019,1,1)
        to_date = date(2019,1,31)
        stock_df = self.h._stock_history(symbol, from_date, to_date)
        self.assertGreaterEqual(len(stock_df), 10)
        self.assertEqual(stock_df['Symbol'].iloc[0], "RELIANCE")
        self.assertEqual(stock_df['Date'].iloc[0], date(2019,1,1))
        self.assertEqual(stock_df['Date'].iloc[-1], date(2019,1,31))

    def tearDown(self):
        self.h.s.close()
