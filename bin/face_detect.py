#/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import cv2
import dlib
import time

local_path = os.path.split(os.path.realpath(__file__))[0]
num = local_path.rfind('/')
local_path = local_path[0:num]
sys.path.append(local_path + "/lib/facepp-python-sdk-master/")

from facepp import API
from facepp import File
import opencvface

POSITIVE_DIR = '../data/positive_samples/'
POSITIVE_SAMPLES = [ os.path.join(POSITIVE_DIR, x) for x in os.listdir(POSITIVE_DIR) if x.find("svn") == -1]
NEGTIVE_DIR = '../data/negtive_samples/'
NEGTIVE_SAMPLES = [ os.path.join(NEGTIVE_DIR, x) for x in os.listdir(NEGTIVE_DIR) if x.find("svn") == -1]

def print_result(hint, result):
    from pprint import pformat
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            d = {}
            for (k, v) in obj.iteritems():
                d[encode(k)] = encode(v)
            #return { encode(k):encode(v) for (k, v) in obj.iteritems() }
            return d
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

def has_big_pic(res_dict):
# 容易引发badcase, 不用
    img_height = res_dict['img_height']
    img_width = res_dict['img_width']
    flag = False
    h = 0
    w = 0
    for face in res_dict['face']:
        height = face['position']['height']
        width = face['position']['width']
        h += height
        w += width
    print h
    print w
    if h  > 10 and w > 10:
        flag = True
    return flag

def has_valid_pic(res_dict):
    if len(res_dict['face']) < 1:
        return False
    #if not has_big_pic(res_dict):
    #    return False
    return True


def facepp_detect():
    API_KEY = '76f2ed8ab272e8793c990ae6c9e0a5e8'
    API_SECRET = 'RdVvpVpLaBYi37eMfGzAa8drJyDtDBpE'
    api = API(API_KEY, API_SECRET)
    count = 0
    for pic in POSITIVE_SAMPLES:
        #if pic != "../data/positive_samples/IMG_7207.JPG":
        #    continue
        st = time.time()
        res =  api.detection.detect(img = File(pic), mode = 'normal')
        print pic,":",(time.time()-st)*1000,"ms"
        if has_valid_pic(res):
            count += 1
            print pic,":YES"
        else:
            print pic,":NO",":",len(res['face'])

    print "True Positive:",round(float(count)*100/len(POSITIVE_SAMPLES),2)
    print "False Negative:",100 - round(float(count)*100/len(POSITIVE_SAMPLES),2)

    count = 0
    for pic in NEGTIVE_SAMPLES:
        #if pic != "../data/negtive_samples/IMG_7404.JPG":
        #    continue
        res =  api.detection.detect(img = File(pic),  mode='normal')
        if not has_valid_pic(res):
            count += 1
            print pic,":YES"
        else:
            print pic,":NO",":",len(res['face'])

    print "True Negative:",round(float(count)*100/len(NEGTIVE_SAMPLES),2)
    print "False Positive:",100 - round(float(count)*100/len(NEGTIVE_SAMPLES),2)

def opencv_detect():
    cascade = cv2.CascadeClassifier("../data/haarcascade_frontalface_alt.xml")
    count = 0
    all_num = 0
    all_time = 0.0
    for pic in POSITIVE_SAMPLES:
        all_num += 1
        #if pic != "../data/positive_samples/IMG_7207.JPG":
        #    continue
        st = time.time()
        try:
            gray = opencvface.load_img(pic)
            res =  opencvface.detect(gray, cascade)
        except Exception,data:
            print "ERROR:",pic
        print pic,":",(time.time()-st)*1000,"ms"
        all_time += (time.time()-st)*1000
        if len(res) > 0:
            count += 1
            print pic,":YES"
        else:
            print pic,":NO",":",len(res)

    print "True Positive:",round(float(count)*100/len(POSITIVE_SAMPLES),2)
    print "False Negative:",100 - round(float(count)*100/len(POSITIVE_SAMPLES),2)

    count = 0
    for pic in NEGTIVE_SAMPLES:
        #if pic != "../data/negtive_samples/IMG_7404.JPG":
        #    continue
        st = time.time()
        all_num += 1
        gray = opencvface.load_img(pic)
        res =  opencvface.detect(gray, cascade)
        print pic,":",(time.time()-st)*1000,"ms"
        all_time += (time.time()-st)*1000
        if len(res) < 1:
            count += 1
            print pic,":YES"
        else:
            print pic,":NO",":",len(res)

    print "True Negative:",round(float(count)*100/len(NEGTIVE_SAMPLES),2)
    print "False Positive:",100 - round(float(count)*100/len(NEGTIVE_SAMPLES),2)

    print "AVG COST:", all_time/ all_num

def dlib_detect():
    detector = dlib.get_frontal_face_detector()
    count = 0
    all_num = 0
    all_time = 0.0
    for pic in POSITIVE_SAMPLES:
        #if pic != "../data/positive_samples/IMG_7207.JPG":
        #    continue
        all_num += 1
        st = time.time()
        try:
            img = cv2.imread(pic)
            st = time.time()
            # the second param means upsample_num_times >=0
            res = detector(img, 0)
        except Exception,data:
            print "ERROR:",pic
        print "pic:",(time.time()-st)*1000,"ms"
        all_time += (time.time()-st)*1000
        if len(res) > 0:
            count += 1
            print pic,":YES"
        else:
            print pic,":NO",":",len(res)

    print "True Positive:",round(float(count)*100/len(POSITIVE_SAMPLES),2)
    print "False Negative:",100 - round(float(count)*100/len(POSITIVE_SAMPLES),2)

    count = 0
    for pic in NEGTIVE_SAMPLES:
        #if pic != "../data/negtive_samples/IMG_7404.JPG":
        #    continue
        all_num += 1
        st = time.time()
        img = cv2.imread(pic)
        res = detector(img, 0)
        print "pic:",(time.time()-st)*1000,"ms"
        all_time += (time.time()-st)*1000
        if len(res) < 1:
            count += 1
            print pic,":YES"
        else:
            print pic,":NO",":",len(res)

    print "True Negative:",round(float(count)*100/len(NEGTIVE_SAMPLES),2)
    print "False Positive:",100 - round(float(count)*100/len(NEGTIVE_SAMPLES),2)
    print "AVG COST:", all_time/ all_num

def test_facepp(pic):
    #pic = '../data/negtive_samples/IMG_7404.JPG'
    #pic = '../data/positive_samples/IMG_7116.JPG'
    API_KEY = '76f2ed8ab272e8793c990ae6c9e0a5e8'
    API_SECRET = 'RdVvpVpLaBYi37eMfGzAa8drJyDtDBpE'
    api = API(API_KEY, API_SECRET)
    res = api.detection.detect(img = File(pic), mode='normal')
    print_result('detect result', res)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:",sys.argv[0],"[facepp|opencv|IMG_PATH]"
        quit()
    if sys.argv[1] == "facepp":
        facepp_detect()
    elif sys.argv[1] == "opencv":
        opencv_detect()
    elif sys.argv[1] == "dlib":
        dlib_detect()
    else:
        test_facepp(sys.argv[1])
