import cv2 as cv
import numpy as np
import csv
import time as tm
import random
from datetime import date
import datetime
import calendar

start_time = tm.time()
video = cv.VideoCapture(0)
ret, frame1 = video.read()
ret, frame2 = video.read()

#These two function provide the day of the week
def get_day():
    current_date = date.today()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    dayOfWeek = dayGetter(day, month, year)
    return dayOfWeek
    
def dayGetter(day, month, year):
    days = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]
    #dayIndex is an object of datetime
    dayIndex = datetime.date(year, month, day)
    # .weekday is a method of this object (returns a number)
    day_of_week = days[dayIndex.weekday()]
    return (day_of_week)


day = get_day()




fps = 0
counter = 0
datastuff = 0
while video.isOpened():
    difference = cv.absdiff(frame1, frame2)
    greyScale = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(greyScale, (1,1), 0)
    dilated = cv.dilate(blurred, None, iterations=1)
    fram3 = cv.Canny(blurred, 125, 175)
    _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(frame1, contours, -1, (0,255,0), 5)
    fps += 1
    for contour in contours:
        
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 900:
            continue

        if (w > 40 and h > 50) and (w < 500 and h < 600):
            cv.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 3)
    cv.imshow("TEST", frame1)
    #cv.imshow("TEST2", fram3)
    frame1 = frame2
    ret, frame2 = video.read()

    #if int(fps)%70==0: 
    if int(tm.time()-start_time)==5:
        start_time=tm.time()
        if(day == "Sun"):
            time = datetime.datetime.now()
            currentTime = "{}:{}".format(time.hour, time.minute)
            # Figure out how to replace zeros with blanks
            row = [currentTime, 0, 0, 0, 0, 0, 4, 0]
            print(f"HI")
            with open("data/test.csv", 'a', newline='') as data:
                writer = csv.writer(data)
                writer.writerow(row)

    #Incrementing the counters and creating a list for a row
        counter = random.randint(1,5000)
        datastuff = random.randint(1,5000)
        row_stuff = [counter,datastuff]
        #Writing into the csv
        #with open("data/test.csv", 'a') as data:
            #writer = csv.writer(data)
            #writer.writerow(row_stuff)
    #if int(tm.time()-start_time)==16:
        #break
    if cv.waitKey(40) & 0xFF==ord('q'):
        break


print(f"The time is {tm.time()}")
cv.destroyAllWindows()
video.release()