import datetime
import time
from functools import partial

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