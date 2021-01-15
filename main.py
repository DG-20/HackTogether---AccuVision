import cv2 as cv
import numpy as np

video = cv.VideoCapture(0)
ret, frame1 = video.read()
ret, frame2 = video.read()


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

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 900:
            continue

        if (w > 400 and h > 500) and (w < 500 and h < 600):
            cv.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 3)
    cv.imshow("TEST", frame1)
    #cv.imshow("TEST2", fram3)
    frame1 = frame2
    ret, frame2 = video.read()

    if cv.waitKey(40) & 0xFF==ord('q'):
        break

cv.destroyAllWindows()
video.release()