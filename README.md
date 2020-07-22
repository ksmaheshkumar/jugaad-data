# Introduction

Jugad data is a library to download historical price-volume data from NSE in pandas dataframe.

[![Build Status](https://travis-ci.org/jugaad-py/jugaad-data.svg?branch=master)](https://travis-ci.org/jugaad-py/jugaad-data)

# Installation

`pip install git+https://github.com/jugaad-py/jugaad-data.git`

# Getting started
```python
from jugaad_data import JugaadData
from datetime import date

j = JugaadData()
symbol = "RELIANCE"
index = "NIFTY 50"
from_date = date(2019,1,3)
to_date = date(2020,1,10)

stock_df = j.stock_history(symbol, from_date, to_date)

index_df = j.index_history(index, from_date, to_date)

print(stock_df.head())
print(index_df.head())
```

# Documentation

Visit https://marketsetup.in/documentation/jugaad-data/ for detailed documentation.

