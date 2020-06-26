import datetime
import time
from functools import partial

from datetime import date, timedelta
import calendar

import numpy as np

def np_float(num):
    try:
        return np.float64(num)
    except:
        return np.nan

def np_date(dt):
    try:
        d = datetime.datetime.strptime(dt, "%d-%b-%Y").date()
        return np.datetime64(d)
    except:
        return np.datetime64("NaT")

def np_int(num):
    try:
        return np.int64(num)
    except:
        return np.int64(0)

def break_dates(from_date, to_date):
    if from_date.replace(day=1) == to_date.replace(day=1):
        return [(from_date, to_date)]
    date_ranges = []
    month_start = from_date
    month_end = month_start.replace(day=calendar.monthrange(month_start.year, from_date.month)[1])
    while(month_end < to_date):
        date_ranges.append((month_start, month_end))
        month_start = month_end + timedelta(days=1)
        month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
        if month_end > to_date:
            date_ranges.append((month_start, to_date))
    return date_ranges


