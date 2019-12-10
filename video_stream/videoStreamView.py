from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from img_pro.utils.camerautil import VideoCamera

# Create your views here.
video_camera = None
global_frame = None



def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
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