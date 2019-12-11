import threading
from img_pro import img_process
from img_pro.img_process import Res10CaffeFaceModel
from imutils.video import VideoStream as VS
import time
import numpy as np
from imutils.video import FPS as FS
import cv2

class MonitoringThread(threading.Thread):
    def __init__(self, name, camera, save_video_path):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self._res={'category':'Mei de ren','probability':''}


    def run(self):
        # 打开视频，获取帧
        vs = VS(src=0).start()
        # 线程休眠，让摄像头启动
        time.sleep(2)
        # 获取帧
        fs = FS().start()
        #读取模型
        model = Res10CaffeFaceModel('img_pro/face_detetor', 'img_pro/face_detetor/deploy.prototxt', 'img_pro/utils', 0.8)
        # 循环遍历视频帧，并进行识别
        while self.isRunning:
            frame = vs.read()
            if frame is None:
                continue
            frame = frame[:, ::-1]
            fs.update()
            self._res, startX, startY, endX, endY = model.predict(frame)
            if self._res["category"] is None:
                self._res["category"] = "Mei de ren"
                self._res["probability"] = ""
            else:
                if self._res["probability"] > 0.8:
                    temp_img = frame.copy()
                    frame = cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
                    # 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
                else:
                    self._res["category"] = "Mo Sheng Ren"
                    self._res["probability"] = ""

            strTip = self._res["category"] + str(self._res["probability"])
            # 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
            frame = cv2.putText(frame, strTip, (startX, startY), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        fs.stop()
        cv2.destroyAllWindows()
        vs.stop()


    def stop(self):
        self.isRunning = False

    def getRes(self):
        return self._res

    def __del__(self):
        pass
