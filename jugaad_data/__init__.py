import csv
import os
import calendar
from io import StringIO
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor

from urllib.parse import urljoin, urlencode

from requests import Session
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

from .util import  np_date, np_float, np_int, break_dates

__version__ = 0.1

class JugaadData:
    headers = {
        "Host": "www1.nseindia.com",
        "Referer": "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        }
    url_map = {
        "stock_history": "/products/dynaContent/common/productsSymbolMapping.jsp",
        "symbol_count": "/marketinfo/sym_map/symbolCount.jsp",
    }
    base_url = "https://www1.nseindia.com"
    cache_dir = ".cache"
    workers = 2
    use_threads = True
    def __init__(self):
        
        self.s = Session()
        self.s.headers.update(self.headers)
        self.symbol_count_map = {}
        self.ssl_verify = True
        try:
            os.mkdir(self.cache_dir)
        except FileExistsError:
            pass

    def html_to_arr(self, html):
        bs = BeautifulSoup(html, features="lxml")
        csv_text = bs.find("div", {"id":"csvContentDiv"}).text.replace(':', '\n')
        f = StringIO(csv_text)
        reader = csv.reader(f)
        arr = [row for row in reader]
        return arr
    
    def arr_to_df(self, arr, dtypes):
        new_arr = []
        for row in arr[1:]:
            new_row = []
            for cell, dtype in zip(row, dtypes):
                new_row.append(dtype(cell))
            new_arr.append(new_row)
        
        return pd.DataFrame(new_arr)
             
    def _get(self, path, params):
        url = urljoin(self.base_url, path)
        return self.s.get(url, params=params, verify=self.ssl_verify)
        
    
    def _stock_history(self, symbol, from_date, to_date, series='EQ'):
        sym_count = self._symbol_count(symbol)
        path = "/products/dynaContent/common/productsSymbolMapping.jsp"
        params = {
                'symbol': symbol,
                'symbolCount': sym_count,
                'fromDate': from_date.strftime('%d-%m-%Y'),
                'toDate': to_date.strftime('%d-%m-%Y'),
                'dataType': 'PRICEVOLUMEDELIVERABLE',
                'dateRange': ' ',
                'series': series,
                'segmentLink': 3, 
        }
        key = "{}_{}_{}_{}".format("stock", symbol, from_date.month, series)

        if from_date.replace(day=1) == to_date.replace(day=1):
            try:
                df = self._cache_read(key)
                return df[df['Date']>=np.datetime64(from_date)][df['Date']<=np.datetime64(to_date)]
            except:
                pass
            
        self.r = self._get(path, params)
        arr = self.html_to_arr(self.r.text)
        dtypes = [  str, str, np_date, np_float,
                    np_float, np_float, np_float,
                    np_float, np_float, np_float,
                    np_int, np_float, np_int,
                    np_int, np_float]
        headers = [ "Symbol", "Series", "Date", "Prev Close", "Open Price",	"High Price",
                    "Low Price", "Last Price",	"Close Price", "VWAP", "Total Traded Quantity", "Turnover",
                    "No. of Trades", "Deliverable Qty", "% Dly Qt to Traded Qty"]
        df = self.arr_to_df(arr, dtypes)
        df.columns = headers
        if (from_date.replace(day=1) == to_date.replace(day=1)) and (from_date.day == 1) and (to_date.day == calendar.monthrange(from_date.year, from_date.month)[1]):
            self._cache_store(df, key)
        return df

    def stock_history(self, symbol, from_date, to_date, series='EQ'):
        date_ranges = break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1], series) for x in date_ranges]
        dfs = self._pool(self._stock_history, params)
        return pd.concat(dfs, ignore_index=True)

    def _index_history(self, symbol, from_date, to_date):
        path = "/products/dynaContent/equities/indices/historicalindices.jsp"
        params = {
            "indexType": symbol,
            'fromDate': from_date.strftime('%d-%m-%Y'),
            'toDate': to_date.strftime('%d-%m-%Y'),
        }
        key = "{}_{}_{}".format("index", symbol, from_date.month)

        if from_date.replace(day=1) == to_date.replace(day=1):
            try:
                df = self._cache_read(key)
                return df[df['Date']>=np.datetime64(from_date)][df['Date']<=np.datetime64(to_date)]
            except:
                pass
        
        self.r = self._get(path, params)
        arr = self.html_to_arr(self.r.text)
        dtypes = [  np_date, np_float, np_float,
                    np_float, np_float, np_int,
                    np_float]
        headers = [ "Date", "Open",	"High",
                    "Low", "Close", "Shares Traded",
                    "Turnover (Rs. Cr)"]
        df = self.arr_to_df(arr, dtypes)
        df.columns = headers
        if (from_date.replace(day=1) == to_date.replace(day=1)) and (from_date.day == 1) and (to_date.day == calendar.monthrange(from_date.year, from_date.month)[1]):
            self._cache_store(df, key)
        return df

    def index_history(self, symbol, from_date, to_date, series='EQ'):
        date_ranges = break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1]) for x in date_ranges]
        dfs = self._pool(self._index_history, params)
        return pd.concat(dfs, ignore_index=True)

    def _fut_opt_df(self, symbol, from_date, to_date, instrument_type, expiry_date, option_type, strike_price):
        sym_count = self._symbol_count(symbol)
        path = "/products/dynaContent/common/productsSymbolMapping.jsp"
        params = {
                'instrumentType': instrument_type,
                'symbol': symbol,
                'expiryDate': expiry_date.strftime('%d-%m-%Y'),
                'optionType': option_type,
                'strikePrice': strike_price,
                'dateRange': ' ',
                'fromDate': from_date.strftime('%d-%m-%Y'),
                'toDate': to_date.strftime('%d-%m-%Y'),
                'segmentLink': 9, 
                'symbolCount': " "
        }
        key = "{}_{}_{}_{}_{}_{}".format(instrument_type, symbol, expiry_date, option_type, strike_price,
                                    from_date.month)

        if from_date.replace(day=1) == to_date.replace(day=1):
            try:
                df = self._cache_read(key)
                return df[df['Date']>=np.datetime64(from_date)][df['Date']<=np.datetime64(to_date)]
            except:
                pass
            
        self.r = self._get(path, params)
        arr = self.html_to_arr(self.r.text)  
        return arr
    
    def fno_dtypes_headers(self, instrument_type):
        return 
    
    def _pool(self, function, params):
        if self.use_threads:
            with ThreadPoolExecutor(max_workers=self.workers) as ex:
                dfs = ex.map(function, *zip(*params))
        else:
            dfs = [self._stock_history(*param) for param in params]
        return dfs
    def _cache_store(self, df, key):
        path = os.path.join(self.cache_dir, key + '.hdf')
        df.to_hdf(path, key="data")
    
    def _cache_read(self, key):
        path = os.path.join(self.cache_dir, key + '.hdf')
        return pd.read_hdf(path, key="data")

    def _symbol_count(self, symbol):
        sym_count = self.symbol_count_map.get(symbol)
        if sym_count:
            return sym_count
        path = "/marketinfo/sym_map/symbolCount.jsp"
        params = {"symbol": symbol}
        self.r = self._get(path, params)
        self.symbol_count_map[symbol] = self.r.text.lstrip().rstrip()
        return self.symbol_count_map[symbol]




