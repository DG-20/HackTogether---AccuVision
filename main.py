import cv2 as cv
import numpy as np

video = cv.VideoCapture()
isTrue, frame1 = video.read()
isTrue, frame2 = video.read()


while video.isOpened():
    Difference = cv.absdiff(frame1, frame2)
    greyScale = cv.cvtColor(Difference, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(greyScale, (5,5), 0)
    thresh = cv.threshold(blurred, 20, 255, cv.THRESh_BINARY)
    dilated = cv.dilate(thresh, NONE, iterations = 3)
    contours = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(frame1, contours, -1, (0,255,0), 2)

    cv.imshow("TEST", frame1)
    frame1 = frame2
    frame2 = video.read()

    if cv.waitKey(40) == 27:
        break

cv.destroyAllWindows()