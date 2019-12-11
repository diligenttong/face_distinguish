import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
import pickle
from User import models
from face_distinguish import settings
from img_pro import img_process
from img_pro.img_process import Res10CaffeFaceModel


# Create your views here.
def familyAddDepartLayer(request):
    ret = {"success": False, "context": {"msg": ""}}
    if request.method == "POST":
        data = json.loads(request.body.decode())
        name = data["name"]
        initial = data["initial"]
        num = models.Family.objects.create(name=name, initial=initial)
        if num:
            ret['success'] = True
            ret['context']['msg'] = '添加成功'
        else:
            ret['success'] = False
            ret['context']['msg'] = '失败了'
        return JsonResponse(ret)
    return render(request, 'family/addDepartLayer.html', locals())


def familyEditDepartLayer(request):
    ret = {"success": False, "context": {"msg": ""}}
    if request.method == "POST":
        data = json.loads(request.body.decode())
        print(data)
        id = data["id"]
        name = data["name"]
        num = models.Family.objects.update(id=id, name=name)
        if num >= 1:
            ret['success'] = True
            ret['context']['msg'] = '编辑成功'
        else:
            ret['success'] = False
            ret['context']['msg'] = '失败了'
        return JsonResponse(ret)

    return render(request, 'family/editDepartLayer.html', locals())


def delete_depart(request):
    ret = {"success": False, "context": {"msg": ""}}
    data = json.loads(request.body.decode())
    id = data['id']
    s = models.Family.objects.filter(id=id).delete()
    if s:
        ret['success'] = True
        ret['context']['msg'] = '删除成功'
    else:
        ret['success'] = False
        ret['context']['msg'] = '删除失败，请重新删除'
    return JsonResponse(ret)


def trainModel(request):
    if request.method == "POST":
        # 读取需要训练的数据
        print("开始")
        paths = img_process.img_path_read("img_pro/train_data")
        path_list = []
        # paths是一个生成器，即类

        for (i, path) in enumerate(paths):
            path_list.append(path)
        # 生成识别类
        print("生成识别类")
        model = Res10CaffeFaceModel('img_pro/face_detetor', 'img_pro/face_detetor/deploy.prototxt', 'img_pro/utils', 0.8)
        # 处理需要训练的图片，并生成LabelX和LabelY
        print("处理需要训练的图片，并生成LabelX和LabelY")
        model.detect_face_to_label(path_list)
        # 将labelX和LabelY写成pickle存在磁盘
        print("将labelX和LabelY写成pickle存在磁盘")
        model.label_to_pickle('img_pro/train_data/pickle_data/data.pickle')
        # 训练人脸识别分类器(不是人脸检测)
        print("开始训练")
        cls = model.train(Res10CaffeFaceModel.FIT_MODEL_SVC, True)
        print("训练结束")
        print("开始写入模型")
        f = open('img_pro/train_data/pickle_data/train.pickle', 'wb')
        f.write(pickle.dumps(cls))
        f.close()
        print("写入模型结束")
        print("训练结束")
        ret = {"success": False, "context": {"msg": ""}}
        if cls:
            ret['success'] = True
            ret['context']['msg'] = '训练成功'
        else:
            ret['success'] = False
            ret['context']['msg'] = '训练失败，请重新训练'
        return JsonResponse(ret)



# class FamilyDetail(views.View):
#     def get(self,request,id):
#         family = models.Family.objects.filter(id=id).first()
#         return render(request, '', locals())
#     def put(self,request,id):
#         name = request.POST['name']
#         photo = request.POST['photo']
#         models.Family.objects.filter(id=id).update(name=name,photo=photo)
#         return redirect('/family/')
#     def delete(self,request,id):
#         models.Family.objects.filter(id=id).delete()
#         return HttpResponse()


