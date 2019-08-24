# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 21:24:55 2019

@author: Administrator
"""
from PIL import Image 
import cv2
import numpy as np 

img = cv2.imread('C:/Users/Administrator/Desktop/test2.jpg')
#save an original copy since the image img is going to get modified during the processing
orig = img.copy()
# convert the image to grayscale, blur it, and find the edges in the image
#The parameter values are carefully chosen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 40, 40, 40)
edges = cv2.Canny(gray,50,200)
#The below two lines are used to convert the array back to image and then display in default viewer
#edges=Image.fromarray(edges)
#edges.show()
minLineLength = 100
maxLineGap = 10
#Find the prominent lines which also include the edge which separates the planes in the two planar image
lines = cv2.HoughLinesP(edges,1,(np.pi)/180,50,minLineLength,maxLineGap)
#Parameters are set such that the horizontal lines are detected which includes the 
#top and bottom edges of the box within which the qr code resides 

for i in range(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
#The for loop is used to mark the lines detected by the hough transform and is optional 
#The lines array is reshaped to 2D array
line = lines.reshape(len(lines),-1)
arr = [0]*len(line)
#Since we are interested only in the y value of the lines so as to 
#finally split the planes and concatenate later
for i in range (0,len(line)):
    j = 1
    arr[i] = line[i][j]
#The sorting will help us to identify the y value of the top and bottom edges
arr.sort()
p = arr[0]
q = arr[len(arr)-1]
r = arr[2]
#r value can be either arr[1] or arr[2] since both indicate the edge separating the planes 
x = orig.shape[1] #for the width of the image
#The top and bottom parts are cropped out of the image
top = orig[p:r, 0:x]
#top=Image.fromarray(top)
#top.show()
bottom = orig[r-1:q, 0:x]
#bottom=Image.fromarray(bottom)
#bottom.show()

# convert the image to grayscale, blur it, and find the edges in the image
tgray = cv2.cvtColor(top,cv2.COLOR_BGR2GRAY)
tgray = cv2.bilateralFilter(tgray, 40, 40, 40)
tedge = cv2.Canny(tgray,50,200)
(thresh, bwt) = cv2.threshold(tedge, 125, 255, cv2.THRESH_BINARY)
#Thresholding is done for the sake of identifying the corner pixels of the top image 
#These for loops are used for the same
for i in range (0,x):
    if (bwt[1][i] == 255):
        a = i
        break
for i in range (x-1,0,-1):
    if (bwt[1][i] == 255):
        b = i
        break
for i in range (0,x):
    if (bwt[bwt.shape[0]-1][i] == 255):
        c = i
        break
for i in range (x-1,0,-1):
    if (bwt[bwt.shape[0]-1][i] == 255):
        d = i
        break
print(a,b,c,d)
#points for warping the image 'top' to a 100*50 array
pts1 = np.float32([[a,1],[b,1],[c+1,bwt.shape[0]-1],[d,bwt.shape[0]-1]])
pts2 = np.float32([[0,0],[100,0],[0,50],[100,50]])
M = cv2.getPerspectiveTransform(pts1,pts2)
tfin = cv2.warpPerspective(top,M,(100,50))
tfin = cv2.cvtColor(tfin, cv2.COLOR_BGR2GRAY)

#The same procedure is used for the bottom image
bgray = cv2.cvtColor(bottom,cv2.COLOR_BGR2GRAY)
bgray = cv2.bilateralFilter(bgray, 40, 40, 40)
bedge = cv2.Canny(bgray,50,200)
(thresh, bwb) = cv2.threshold(bedge, 125, 255, cv2.THRESH_BINARY)

for i in range (0,x):
    if (bwb[0][i] == 255):
        e = i
        break
for i in range (x-1,0,-1):
    if (bwb[0][i] == 255):
        f = i
        break
for i in range (0,x):
    if (bwb[bwb.shape[0]-2][i] == 255):
        g = i
        break
for i in range (x-1,0,-1):
    if (bwb[bwb.shape[0]-2][i] == 255):
        h = i
        break
print(e,f,g,h)

pts1 = np.float32([[e,0],[f,0],[g,bwb.shape[0]-1],[h,bwb.shape[0]-1]])
pts2 = np.float32([[0,0],[100,0],[0,50],[100,50]])
M = cv2.getPerspectiveTransform(pts1,pts2)
bfin = cv2.warpPerspective(bottom,M,(100,50))
bfin = cv2.cvtColor(bfin, cv2.COLOR_BGR2GRAY)

#Finally the two images are concatenated to form the complete image(100*100)
final = np.concatenate((tfin, bfin), axis=0)
final = Image.fromarray(final)
final.show()
