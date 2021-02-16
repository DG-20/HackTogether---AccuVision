from datetime import date
import datetime
import calendar

# These two functions provide the day of the week and the index associated with that day
def get_day():
    current_date = date.today()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    dayOfWeek = dayGetter(day, month, year)
    return dayOfWeek

def dayGetter(day, month, year):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # dayIndex is an object of datetime
    dayIndex = datetime.date(year, month, day)
    dayNum = dayIndex.weekday()
    # .weekday is a method of this object (returns a number)
    day_of_week = days[dayIndex.weekday()]
    return (day_of_week, dayNum)
   