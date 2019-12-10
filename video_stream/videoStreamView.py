from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from img_pro.utils.camerautil import VideoCamera

from django.http import JsonResponse

import cv2

# Create your views here.
video_camera = None
global_frame = cv2.imread('video_stream/video.jpg')
ret, global_frame = cv2.imencode('.jpg', global_frame)
global_frame=global_frame.tobytes()



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

