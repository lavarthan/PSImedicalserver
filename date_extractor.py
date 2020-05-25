from datetime import date
import calendar


# a = input("enter day:")
def date_extractor(a):
    a.lower()
    my_date = date.today()
    today = calendar.day_name[my_date.weekday()].lower()

    from datetime import datetime, timedelta
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    day_want = days.index(a) - days.index(today)
    if day_want <= 0:
        day_want += 7
    N = day_want

    date_N_days_after = datetime.now() + timedelta(days=N)
    # print(datetime.now().strftime('%m/%d/%Y'))
    return date_N_days_after.strftime('%m/%d/%Y')
