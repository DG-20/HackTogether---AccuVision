import cv2 as cv
import csv
import time as tm
import random
from datetime import date
import datetime
from dayGetter import get_day
import gspread as GS

# Enables Google API linking to AccuVision
gc = GS.service_account(filename='creds.json')

# Starting the time in order to check for time elapsed further down the code.
start_time = tm.time()

# Reads the sample video and splits into frames
video = cv.VideoCapture("videos/hacktogehtt4.mp4")
ret, frame1 = video.read()
ret, frame2 = video.read()
person_counter = 0
PositionMarker = ""

# Creates a new CSV file with the required headers
row = ["Time of Day", "Monday", "Tuesday", "Wednesday",
       "Thursday", "Friday", "Saturday", "Sunday"]
with open("data/week1.csv", 'a', newline='') as data:
    writer = csv.writer(data)
    writer.writerow(row)

windowWidth = frame1.shape[1]
windowHeight = frame1.shape[0]

# This initially sets the previous_x (used later) to half the window width
previous_x = windowWidth/2

# Booleans that are used later on
going_left = False
going_right = False

counter = 0
contourCount = 0

# Bulk of the processing and analysis
while video.isOpened():
    going_left = False
    going_right = False

    # Using the get_day function from dayGetter.py to retrieve tuple
    dayTuple = get_day()
    dayNum = dayTuple[1]

    counter += 1

    # Frame by frame analysis through absdiff, greyscaling, blurring, dilation, canny, thresholding, and contouring in order to detect and track movement.
    difference = cv.absdiff(frame1, frame2)
    greyScale = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(greyScale, (21, 21), 0)
    dilated = cv.dilate(blurred, None, iterations=1)
    fram3 = cv.Canny(blurred, 125, 175)
    _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(
        dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Updating the position marker based on the motion detection using contours.
    if len(contours) < 1:
        PositionMarker = "NO MOTION"

    # Printing on the screen of the video feed to show status and live counter.
    cv.putText(frame1, f"# PEOPLE: {person_counter}", (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv.LINE_AA)
    cv.putText(frame1, f"STATUS: {PositionMarker}", (315, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv.LINE_AA)

    # Algorithm for addition/subtraction of live counter based on positioning of bounding box.
    # In this configuration, going to the left counted as an increment in the counter and going to the right counted as a decrement in the counter.
    for contour in contours:

        # Obtain coordinates of bounding box if the bound area is greater than 10000 (can be customized based on configuration)
        (x, y, w, h) = cv.boundingRect(contour)
        if cv.contourArea(contour) > 10000:

            # Drawing the bounding box
            cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 3)
            contourCount += 1

            # For the first iteration, set the previous_x to x
            if contourCount == 1:
                previous_x = x

            # If the current x-value is greater than the previous x-value, set going_right boolean to true and display that in the video feed.
            if previous_x < x:
                PositionMarker = "Going Right"
                going_right = True

             # If the current x-value is lesser than the previous x-value, set going_left boolean to true and display that in the video feed.
            elif previous_x > x:
                PositionMarker = "Going Left"
                going_left = True

            # Increment counter if going left and pass the left boundary condition.
            if going_left == True:
                if (x > 150 and x < 165):
                    person_counter += 1
                    going_left = False

            # Decrement counter if going right and pass the right boundary condition.
            if going_right == True:
                if x + w > windowWidth - 165 and x + w < windowWidth - 160:
                    if person_counter <= 0:
                        person_counter = 0
                    else:
                        person_counter -= 1
                    going_right = False

            # On every third iteration of the while loop, set previous_x to current x.
            if counter % 3 == 0:
                previous_x = x

    resize = cv.resize(frame1, (640, 480))
    cv.imshow("frame1", resize)

    # Setting the next frame as the previous and obtaining the frame after that into frame2 to continue the comparison.
    frame1 = frame2
    ret, frame2 = video.read()

    currentTime = "0:0"

    # Updates every 10 seconds for demonstration purposes, however in the sample csv data, we assumed data updated every five minutes.
    if int(tm.time()-start_time) == 10:
        start_time = tm.time()

        time = datetime.datetime.now()

        # Formatting the Time of Day column for the CSVs.
        if time.minute < 10:
            currentTime = "{}:0{}".format(time.hour, time.minute)
        else:
            currentTime = "{}:{}".format(time.hour, time.minute)

        # After a week of continual running of the code, this section switches to the second CSV file to store two consecutive weeks' data.
        if int(tm.time() - start_time) >= 604800:
            file = open("data/week2.csv")
            reader = csv.reader(file)
            lines = len(list(reader))

            # If the file is currently blank, write the header contained in the row variable.
            if lines == 0:
                writer = csv.writer(file)
                writer.writerow(row)

            # Add a row with the person_counter into the CSV.
            row = [currentTime, None, None, None, None, None, None, None]
            row[dayNum + 1] = person_counter
            with open("data/week2.csv", 'a', newline='') as data:
                writer = csv.writer(data)
                writer.writerow(row)

            # This is utiizing the Google Drive API and uploading the CSV to a Google Sheets to be used by app.py.
            previousWeekData = open("data/week2.csv", 'r').read()
            gc.import_csv(
                '1N4J66C5DeCKBCmroZciQfjj9bEl8FZDhtZor4bYL8Hc', previousWeekData)

            # If in the first week of run-time, use the week1.csv file.
        else:
            row = [currentTime, None, None, None, None, None, None, None]
            row[dayNum + 1] = person_counter
            with open("data/week1.csv", 'a', newline='') as data:
                writer = csv.writer(data)
                writer.writerow(row)

            # This is uploading the CSV to a Google Sheets for week 1.
            currentWeekData = open("data/week1.csv", 'r').read()
            gc.import_csv(
                '1hgcC3dLOoQFVB5-EbkkKNQlFo5GQrcCFzzOsmUSUSWY', currentWeekData)

    # Quits the video feed with 'q'
    if cv.waitKey(40) & 0xFF == ord('q'):
        break

# Destroys (closes) all open video feeds.
cv.destroyAllWindows()
video.release()
