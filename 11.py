# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 17:10:04 2019

@author: Administrator
"""
from PIL import Image
import imutils
import numpy as np
import cv2

image = cv2.imread('C:/Users/Administrator/Desktop/test1.jpg')
ratio = image.shape[0] / 300.0
image = imutils.resize(image, height = 300)
orig = image.copy()
# convert the image to grayscale, blur it, and find the edges in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 10, 30, 30)
edged = cv2.Canny(gray, 50, 200)

# find contours in the edged image, keep only the largest ones, and initialize the qr code contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
screenCnt = None

#loop over our contours
for c in cnts:
	#Approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)
	#If our approximated contour has four points, then
	#we can assume that we have found the qr code
    if len(approx) == 4:
        screenCnt = approx
        break
cv2.drawContours(image, screenCnt, -1, (0, 255, 0), 3)

#Now that we have our screen contour, we need to determine the top-left, top-right, 
#bottom-right, and bottom-left  points so that we can later warp the image
pts = screenCnt.reshape(4, 2)
rect = np.zeros((4, 2), dtype = "float32")
 
#The top-left point has the smallest sum whereas the bottom-right has the largest sum
s = pts.sum(axis = 1)
rect[0] = pts[np.argmin(s)]
rect[3] = pts[np.argmax(s)]
 
#Compute the difference between the points -- the top-right will have the minumum difference
#and the bottom-left will have the maximum difference
diff = np.diff(pts, axis = 1)
rect[1] = pts[np.argmin(diff)]
rect[2] = pts[np.argmax(diff)]
print (rect)

pts1 = rect
pts2 = np.float32([[0,0],[200,0],[0,200],[200,200]])
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(orig,M,(200,200))
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

#optional, for sharpening the image 
#kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
#dst = cv2.filter2D(dst, -1, kernel)

dst = Image.fromarray(dst)
dst.show()