from io import StringIO
import csv

from urllib.parse import urljoin, urlencode

from requests import Session
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

from util import  np_date, np_float, np_int

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

    def __init__(self):
        
        self.s = Session()
        self.s.headers.update(self.headers)
        self.symbol_count_map = {}
        self.ssl_verify = True

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
        self.r = self._get(path, params)
        arr = self.html_to_arr(self.r.text)
        dtypes = [str,
                str,
                np_date,
                np_float,
                np_float,
                np_float,
                np_float,
                np_float,
                np_float,
                np_float,
                np_int,
                np_float,
                np_int,
                np_int,
                np_float]
        df = self.arr_to_df(arr, dtypes)
        return df

        
    def _symbol_count(self, symbol):
        sym_count = self.symbol_count_map.get(symbol)
        if sym_count:
            return sym_count
        path = "/marketinfo/sym_map/symbolCount.jsp"
        params = {"symbol": symbol}
        self.r = self._get(path, params)
        self.symbol_count_map[symbol] = self.r.text.lstrip().rstrip()
        return self.symbol_count_map[symbol]




if __name__=="__main__":
    import time
    from datetime import date

    z = JugaadData()
    z.base_url = "https://23.54.86.108"
    z.ssl_verify = False
    from_date = date(2020,1,1)
    to_date = date(2020,1,30)

    r = z._stock_history("SBIN", from_date, to_date)

    # self.
    # s.headers.update(headers)
    # # url = "https://23.54.86.108/products/dynaContent/common/productsSymbolMapping.jsp?symbol=SBIN&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=02-03-2020&toDate=08-03-2020&dataType=PRICEVOLUME"
    # url = "https://23.54.86.108/products/content/equities/equities/eq_security.htm"
    # #print('--')
    # r = s.get(url, verify=False)
    # print(r.text)