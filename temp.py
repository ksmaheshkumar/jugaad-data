from datetime import date, timedelta
import calendar
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


from_date = date(2019,1,31)
to_date = date(2020,1,1)

print(break_dates(from_date, to_date))