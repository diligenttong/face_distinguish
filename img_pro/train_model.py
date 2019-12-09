#模型训练
from Test_Fxd.img_process import Res10CaffeFaceModel
model = Res10CaffeFaceModel('./face_detetor','./face_detetor/deploy.prototxt','./utils',0.8)
model.collection_photos('./train_data/ypj')
