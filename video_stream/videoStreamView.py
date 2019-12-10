from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from img_pro.utils.camerautil import VideoCamera
import os

from django.http import JsonResponse

import cv2

#模型训练
from img_pro.img_process import Res10CaffeFaceModel



# Create your views here.
video_camera = None
global_frame = cv2.imread('video_stream/video.jpg')
ret, global_frame = cv2.imencode('.jpg', global_frame)
global_frame=global_frame.tobytes()

collection_global_frame =None
model = None






def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True :
        frame = video_camera.get_frame()
        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

def videoViewer(request):
    return StreamingHttpResponse(video_stream(),
                          content_type='multipart/x-mixed-replace; boundary=frame')

import json
def videoViewerState(request):
    if request.method == 'POST':
        global video_camera
        if video_camera is None:
            video_camera = VideoCamera()
        data = json.loads(request.body.decode())
        play_state = data['play_state']
        video_camera.set_play_state(play_state)
        ret = {'success':True,'context':{}}
        return JsonResponse(ret)


def collection_video_stream(path):
    global model
    if model is None:
        model = Res10CaffeFaceModel('img_pro/face_detetor', 'img_pro/face_detetor/deploy.prototxt', 'img_pro/utils',
                                    0.8)
    imgCount = 0
    frameCount = 0
    model.start()
    while True :
        frame, roi_img = model.get_frame_face()
        frameCount+=1
        ret, frame = cv2.imencode('.jpg', frame)
        frame = frame.tobytes()
        if frame is not None:
            if frameCount %10 ==0 and frameCount<=100 and (roi_img is not None):
                cv2.imwrite(path + '/' + str(imgCount) + ".png", roi_img)
                imgCount += 1
            collection_global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + collection_global_frame + b'\r\n\r\n')


def videoCollectionInfoLayer(request):
    return render(request, 'family/collectionInfoLayer.html', locals())

#此处调用信息采集
def videoCollectionInfo(request):
    # data = json.loads(request.body.decode())
    # initial = data['initial']
    initial=request.GET['initial']
    path = 'img_pro/train_data/' + initial
    if not os.path.exists(path):
        os.makedirs(path)
    return StreamingHttpResponse(collection_video_stream(path),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def videoCollectionInfoStop(request):
    global model
    print("hhhhh")
    if model is not None:
        model.stop()


