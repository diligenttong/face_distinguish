#视频模块，包含视频读取，视频处理等等
import cv2 as cv


def face_collection():
    face_cascade = cv.CascadeClassifier('../cascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('../cascades/haarcascade_eye.xml')
    camera = cv.VideoCapture(0)  # 参数表示要使用的摄像头，0表示第一个摄像头
    frameCount=0
    imgCount = 0
    while (True):
        # read函数捕获帧，第一个值为boolean,表示是否捕获成功，第二个为帧本身
        ret, frame = camera.read()
        #  cv.imshow("Image", frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        frameCount += 1

        # 进行实际人脸检测，传递参数 scaleFactor,minNeighbors
        # 分别表示人脸检测过程中每次迭代图像的压缩率以及每个人脸矩形保留近邻数目的最小值,
        #minSize和maxSize用来限制得到的目标区域的范围
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=3, minSize=(50, 50))
        for (x, y, w, h) in faces:
            x -= 40
            y -= 70
            w += 80
            h += 200
            temp_img=frame.copy()
            img = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_img = temp_img[y:y + h, x:x + w]
            if frameCount%10==0 and imgCount <= 100:
                cv.imwrite("train_img/zct/"+str(imgCount)+".png",roi_img)
                imgCount+=1
        cv.imshow("camera", frame)
        if cv.waitKey(1) & 0xff == ord("q"):
            break

    camera.release()
    cv.destroyAllWindows()

def face_detection():
    face_cascade=cv.CascadeClassifier('../cascades/haarcascade_frontalface_default.xml')
    eye_cascade=cv.CascadeClassifier('../cascades/haarcascade_eye.xml')
    camera=cv.VideoCapture(0)  #参数表示要使用的摄像头，0表示第一个摄像头
    while(True):
        #read函数捕获帧，第一个值为boolean,表示是否捕获成功，第二个为帧本身
        ret,frame=camera.read()
        #  cv.imshow("Image", frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 进行实际人脸检测，传递参数 scaleFactor,minNeighbors
        # 分别表示人脸检测过程中每次迭代图像的压缩率以及每个人脸矩形保留近邻数目的最小值
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # 眼睛检测
        for (x, y, w, h) in faces:
            img = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            # 循环输出检测眼睛的结果
            cv.imshow("camera", frame)
            if cv.waitKey(1) & 0xff == ord("q"):
                break

    camera.release()

    cv.destroyAllWindows()

face_collection()