import cv2
import numpy as np
import os

'''
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) - германия
ret, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV) - негатив
ret, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC) - +белый - белый
ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO) недогермания
ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV) - зелёнка'''

hsv = cv2.imread('27.jpg')
hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
cv2.imshow('bin', hsv)
tr = cv2.inRange(hsv, (30, 0,0), (90, 255, 255))
cv2.imshow('bin', hsv)
hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
img = cv2.imread('pedistrain.jpg', cv2.IMREAD_GRAYSCALE)

cv2.imshow('', hsv)
cv2.waitKey(0)


for file in os.listdir("C:\\Users\\Ялицей\\Desktop\\ml_school-main\\data\\training\\a_unevenness"):
    original = cv2.imread(file)
    print(type(original))
    print(type(tr))

# cap = cv2.VideoCapture(0)
# running = True
# while (running):
#     ret, frame = cap.read()
#     ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_TOZERO_INV)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('Video', frame)
#     # cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         running = False

cap.release()
cv2.destroyAllWindows()