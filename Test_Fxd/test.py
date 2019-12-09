from Test_Fxd import img_process
from Test_Fxd.img_process import Res10CaffeFaceModel
from imutils.video import VideoStream as VS
import time
import numpy as np
from imutils.video import FPS as FS
import cv2


from PIL import Image, ImageDraw, ImageFont #opencv.putText不支持中文，需要用这个转一下

#cv2.imencode（）函数转换成jpg

#读取需要训练的数据
print("开始")
paths=img_process.img_path_read("./train_data")
path_list=[]
#paths是一个生成器，即类

for(i, path) in enumerate(paths):
    path_list.append(path)
#生成识别类
print("生成识别类")
model = Res10CaffeFaceModel('./face_detetor','./face_detetor/deploy.prototxt','./utils',0.8)
#处理需要训练的图片，并生成LabelX和LabelY
print("处理需要训练的图片，并生成LabelX和LabelY")
model.detect_face_to_label(path_list)
#将labelX和LabelY写成pickle存在磁盘
print("将labelX和LabelY写成pickle存在磁盘")
model.label_to_pickle('./train_data/pickle_data/data.pickle')
#训练人脸识别分类器(不是人脸检测)
print("开始训练")
cls=model.train(Res10CaffeFaceModel.FIT_MODEL_SVC, True)

#打开视频，获取帧
vs = VS(src=0).start()
#线程休眠，让摄像头启动
time.sleep(2)
#获取帧
fs = FS().start()

#循环遍历视频帧，并进行识别
while(True):
    frame = vs.read()
    frame = frame[:,::-1]
    fs.update()
    res,startX,startY,endX,endY=model.predict(frame)
    if res["category"] is None:
        res["category"] = "Mei de ren"
        res["probability"] = ""
    else:
        if res["probability"] > 0.8:
            temp_img = frame.copy()
            frame = cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            # 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
        else:
            res["category"]="Mo Sheng Ren"
            res["probability"]=""

    strTip = res["category"] + str(res["probability"])
    # 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
    frame = cv2.putText(frame, strTip, (startX,startY), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
fs.stop()
cv2.destroyAllWindows()
vs.stop()



