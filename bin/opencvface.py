#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import cv2
import time


def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()

def draw_str(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)


def detect(img, cascade):
    st = time.time()
    #rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=3, minSize=(0, 0), flags = cv2.CASCADE_SCALE_IMAGE)
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=2, minSize=(10, 10), flags = cv2.CASCADE_SCALE_IMAGE)
    print len(rects)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def load_img(img):
    image = cv2.imread(img)
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return gray

def detect_face(img):
    cascade = cv2.CascadeClassifier("../data/haarcascade_frontalface_alt.xml")
  # Format & size
    image = cv2.imread(img)
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    t = clock()
    rects = detect(gray, cascade)
    vis = image.copy()
    draw_rects(vis, rects, (0, 255, 0))
    dt = clock() - t
    draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
    cv2.imshow('facedetect', vis)
    cv2.waitKey(0)

def main():
    input_file = sys.argv[1]
    detect_face(input_file)

if __name__ == "__main__":
  main()
