import cv2
import numpy as np

myColors = {
    'yellow' : [32,46,167,65,88,249],
    'pink' : [151, 134, 134, 169, 211, 229],
    'pink2' : [164,139,93,170,171,239],
    'pink3' : [141, 46, 192, 172, 158, 227],
    'blue' : [101, 114, 55, 112, 202, 198]
}

coloured_points = []


def getContour(img) :
    areas = []
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    x,y,w,h = 0,0,0,0
    for cnt in contours :
        area = cv2.contourArea(cnt)
        areas.append(area)
        

    if areas :
        cnt = contours[areas.index(max(areas))]
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 1)
    return x+w//2, y

def findColor(img, color) :
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array(myColors[color][0:3])
    upper = np.array(myColors[color][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow('mask', mask)
    x,y = getContour(mask)
    coloured_points.append((x,y))
    for point in coloured_points :
        cv2.circle(imgResult, point, 9, (0,255,0), -1, cv2.LINE_AA)


# url = 'http://192.168.1.104:8080/video'  -- this line can be used to access camera of a mobile using an app and then giving url in below line in place of 0
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 150)
while True :
    success, img = cap.read()
    img = cv2.resize(img, (640,480))
    img = cv2.flip(img, 1)
    imgResult = img.copy()
    findColor(img, 'blue')
    cv2.imshow("result", imgResult)
    if cv2.waitKey(1) == ord('q') :
        break

cv2.destroyAllWindows()
cap.release()