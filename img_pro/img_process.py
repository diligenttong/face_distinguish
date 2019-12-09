#https://blog.csdn.net/learning_tortosie/article/details/85121576
#需要安装模块如下:
"""
pip install opencv-python 基本库(main库）
pip install opencv-contrib-python （main + contrib，即opencv_contribute模块)
#使用清华的镜像文件安装，因为pip太慢了
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-contrib-python

（pip 版本低，可能安装失败，先更新pip
python -m pip install --default-timeout=1000 --upgrade pip
）
"""
"""
思路：先检测出需要训练的图片中的人脸，将人脸区域识别出来，然后将人脸区域的数据，
弄成128维的数组，和其标签保存。
"""

import imutils as IT
from imutils import paths
from imutils.video import VideoStream as VS
from imutils.video import FPS as FS
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import time
import os

import cv2

#支持向量机
from sklearn.svm import SVC
#神经网络
from sklearn.neural_network import MLPClassifier

"""

"""
class Res10CaffeFaceModel:

    FIT_MODEL_SVC = 0
    FIT_MODEL_EIGEN = 1
    FIT_MODEL_FISHER = 2
    FIT_MODEL_LBPH = 3

    #opencv调用Caffe、TensorFlow、Torch、PyTorch训练好的模型
    def __init__(self,faceDetectModelPath,deployPath,face2DataModelPath,confidence=0.5):
        #训练好的人脸检测分类器模型路径
        self._faceDetectModelPath = faceDetectModelPath+'/res10_300x300_ssd_iter_140000.caffemodel'
        #根据存储的内容来看应该是记录了生成的深度神经网络结构，即神经网络的信息
        self._deployPath = deployPath
        self._face2DataModelPath = face2DataModelPath+'/openface_nn4.small2.v1.t7'
        self._confidence = confidence
        self._faceDetectModel = cv2.dnn.readNetFromCaffe(self._deployPath,self._faceDetectModelPath)
        self._face2DataModel = cv2.dnn.readNetFromTorch(self._face2DataModelPath)
        self._lableEncoding = None #y编码器


        self._labelX = []
        self._labelY = []
        self._num = 0
        self._pickelDataPath = ''
        self._recognizer=None  #训练好的模型
        self._fit_model=None   #训练时使用的模型


    def getLabelX(self):
        return self._labelX

    def getLabelY(self):
        return self._labelY

    def getRecognizer(self):
        return self._recognizer

    def getFaceDetectModel(self):
        return self._faceDetectModel

    def getFace2DataModel(self):
        return self._face2DataModel

    def detect_face_to_label(self,path_list):
        if len(path_list) <= 0:
            print("检测图片为空")
            return
        # path ./train_data\xt\0.png
        for path in path_list:
            # img_url_name ['./train_data', 'xt', '0.png']
            img_url_name = path.split(os.path.sep)

            img_dir = img_url_name[0]
            img_labelY = img_url_name[1]
            img_name = img_url_name[2]

            print(img_labelY)

            img = cv2.imread(path)
            cv2.imshow("test",img)
            img = IT.resize(img, width=600)
            img_h, img_w, img_channel = img.shape
            img_blob = cv2.dnn.blobFromImage(
                cv2.resize(img, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)
            # 输入待识别
            self._faceDetectModel.setInput(img_blob)
            #分类预测，输出前向传播的预测(检测)结果 ，计算输出
            detections = self._faceDetectModel.forward()
            if len(detections) > 0:
                # TODO
                #假设每个图像只有一张脸，找到概率最大的边界框
                index=np.argmax(detections[0,0,:,2])
                confidence = detections[0, 0, index, 2]
                print("有人脸，概率为:",confidence)
                #保证检测出的概率也最大表示我们的最小概率测试(因此有助于过滤掉弱信号检测)
                if confidence>self._confidence:
                    #计算出脸的边界框的x,y坐标
                    #TODO
                    box = detections[0, 0, index, 3:7] * np.array([img_w, img_h, img_w, img_h])
                    (startX, startY, endX, endY) = box.astype("int")
                    #提取出面部ROI,然后获得面部ROI维度
                    face=img[startY:endY,startX:endX]
                    (f_h,f_w)=face.shape[:2]
                    #确保脸部的宽高足够大
                    if f_w < 20 or f_h < 20:
                        continue

                    #为人脸ROI构造一个blob，然后通过我们的人脸嵌入模型传递该blob，得到人脸的128-d维度量化
                    face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96,96),(0,0,0),swapRB=True,crop=False)
                    self._face2DataModel.setInput(face_blob)
                    vector128D = self._face2DataModel.forward()
                    # // 测试推理时间
                    # totalTime = self._face2DataModel.getPerfProfile(NULL);
                    #flatten是numpy.ndarray.flatten的一个函数，即返回一个一维数组。
                    self._labelX.append(vector128D.flatten())
                    self._labelY.append(img_labelY)
                    self._num += 1

    def label_to_pickle(self,output_path):
        if bool(output_path) is False:
            output_path = './data.pickle'
        if len(self._labelX) <= 0 or len(self._labelY) <= 0:
            print("生成没有标签,重新检测")
            return
        self._pickelDataPath=output_path
        data = {'labelX': self._labelX, 'labelY': self._labelY}
        file = open(output_path, 'wb')
        file.write(pickle.dumps(data))
        file.close()

    """
    特征脸法（Eigenface）pca
    Local Binary Pattern即局部二值模式
    """
    def train(self,fit_model =FIT_MODEL_SVC,selfData=True,data_path=None,):
        data=None
        if selfData is False:
            if bool(data_path) is False:
                data = pickle.loads(open(self._pickelDataPath, 'rb').read())
            else:
                data = pickle.loads(open(data_path, 'rb').read())
        else:
            data = {'labelX': self._labelX, 'labelY': self._labelY}

        self._lableEncoding = LabelEncoder()
        #编码y标签
        labelys= self._lableEncoding.fit_transform(data['labelY'])
        self._recognizer = None
        self._fit_model = fit_model
        if fit_model == Res10CaffeFaceModel.FIT_MODEL_SVC:
            self._recognizer = SVC(C=1.0, kernel="linear", probability=True)
            self._recognizer.fit(data['labelX'], labelys)
            return self._recognizer

        if fit_model == Res10CaffeFaceModel.FIT_MODEL_EIGEN:
            self._recognizer = cv2.face.EigenFaceRecognizer_create()
            self._recognizer.train(np.asarray(data['labelX']),np.asarray(labelys))

        if fit_model == Res10CaffeFaceModel.FIT_MODEL_FISHER:
            self._recognizer = cv2.face.FisherFaceRecognizer_create()
            self._recognizer.train(np.asarray(data['labelX']), np.asarray(labelys))
        if fit_model == Res10CaffeFaceModel.FIT_MODEL_LBPH:
            self._recognizer = cv2.face.LBPHFaceRecognizer_create()
            self._recognizer.train(np.asarray(data['labelX']), np.asarray(labelys))

    def predict(self,img):

        sx,sy,ex,ey=0,0,56,20
        res={'category':None,'probability':None}

        #预测的时候，将图片进行和训练时候同样的处理
        #将帧传进来，再此处识别人脸，然后图片处理，然后预测
        img = IT.resize(img, width=600)
        img_h, img_w, img_channel = img.shape
        img_blob = cv2.dnn.blobFromImage(
            cv2.resize(img, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)
        # 输入待识别
        self._faceDetectModel.setInput(img_blob)
        # 分类预测，输出前向传播的预测(检测)结果 ，计算输出
        detections = self._faceDetectModel.forward()
        if len(detections) > 0:
            # TODO
            # 假设每个图像只有一张脸，找到概率最大的边界框
            index = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, index, 2]
            # 保证检测出的概率也最大表示我们的最小概率测试(因此有助于过滤掉弱信号检测)
            if confidence > self._confidence:
                # 计算出脸的边界框的x,y坐标
                # TODO
                box = detections[0, 0, index, 3:7] * np.array([img_w, img_h, img_w, img_h])
                (startX, startY, endX, endY) = box.astype("int")
                (sx,sy,ex,ey) = box.astype("int")
                # 提取出面部ROI,然后获得面部ROI维度
                face = img[startY:endY, startX:endX]
                (f_h, f_w) = face.shape[:2]
                # 确保脸部的宽高足够大
                if f_w < 20 or f_h < 20:
                    return (res, sx, sy, ex, ey)

                # 为人脸ROI构造一个blob，然后通过我们的人脸嵌入模型传递该blob，得到人脸的128-d维度量化
                face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
                self._face2DataModel.setInput(face_blob)
                vector128D = self._face2DataModel.forward()

                if self._fit_model == Res10CaffeFaceModel.FIT_MODEL_SVC:
                    #预测predict()返回的是标签，predict_proba()返回的是属于各标签的概率
                    preds=self._recognizer.predict_proba(vector128D)[0]

                    #选取概率最大的最大的下标
                    j = np.argmax(preds)
                    proba = preds[j] #概率
                    res["category"] = self._lableEncoding.classes_[j]
                    res["probability"] = proba

                if self._fit_model == Res10CaffeFaceModel.FIT_MODEL_EIGEN or \
                   self._fit_model == Res10CaffeFaceModel.FIT_MODEL_FISHER or \
                   self._fit_model == Res10CaffeFaceModel.FIT_MODEL_LBPH:
                    pre=self._recognizer.predict(vector128D) #[类别，准确率]
                    print(pre)
                    res["category"] = self._lableEncoding.classes_[pre[0]]
                    res["probability"] = pre[1]

        return (res, sx, sy, ex, ey)


    def collection_photos(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        vs = VS(src=0).start()
        time.sleep(2)
        fs = FS().start()
        imgCount = 0
        frameCount = 0
        while (True):
            frame = vs.read()
            frameCount += 1
            img = frame
            fs.update()
            img = IT.resize(img, width=600)
            img_h, img_w, img_channel = img.shape
            img_blob = cv2.dnn.blobFromImage(
                cv2.resize(img, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)
            # 输入待识别
            self._faceDetectModel.setInput(img_blob)
            detections = self._faceDetectModel.forward()
            if len(detections) > 0:
                index = np.argmax(detections[0, 0, :, 2])
                confidence = detections[0, 0, index, 2]
                if confidence > self._confidence:
                    # 计算出脸的边界框的x,y坐标
                    box = detections[0, 0, index, 3:7] * np.array([img_w, img_h, img_w, img_h])
                    (startX, startY, endX, endY) = box.astype("int")
                    startX -= 40
                    startY -= 70
                    endX += 80
                    endY += 200
                    temp_img = frame.copy()
                    img = cv2.rectangle(frame, (startX, startY), (endX,endY), (255, 0, 0), 2)
                    roi_img = temp_img[startY:endY, startX:endX]
                    if frameCount % 10 == 0 and imgCount <= 100:
                       cv2.imwrite(path + '/' + str(imgCount) + ".png", roi_img)
                       imgCount += 1
            cv2.imshow("Collection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        fs.stop()
        cv2.destroyAllWindows()
        vs.stop()














"""
cv2.dnn.blobFromImage
第一个参数，InputArray image，表示输入的图像，可以是opencv的mat数据类型。
第二个参数，scalefactor，这个参数很重要的，如果训练时，是归一化到0-1之间，那么这个参数就应该为0.00390625f （1/256），否则为1.0
第三个参数，size，应该与训练时的输入图像尺寸保持一致。
第四个参数，mean，这个主要在caffe中用到，caffe中经常会用到训练数据的均值。tf中貌似没有用到均值文件。
第五个参数，swapRB，是否交换图像第1个通道和最后一个通道的顺序。
第六个参数，crop，如果为true，就是裁剪图像，如果为false，就是等比例放缩图像。
"""


"""
文件夹内图片路径读取
"""
def img_path_read(url=""):
    if url == "":
        url="./"
    return paths.list_images(url)





"""
图标处理
"""
def img_processor(url):
    if url == "" or url==None:
        return
    img_url_name=url.split(os.path.sep)
    img_name=img_url_name[1]
    img_url = img_url_name[0].split('/')[1]
    print(img_url)
    img = cv2.imread(url)
    img=IT.resize(img,width=600)

    img_h,img_w,img_channel=img.shape

    image_blob= cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)
    # cv2.imshow("Test0",image_blob[0][0])
    # cv2.imshow("Test1", image_blob[0][1])
    # cv2.imshow("Test3", image_blob[0][2])
    # cv2.waitKey()


