from django.shortcuts import render,redirect,HttpResponse
from django import views
from User import models
from face_distinguish import settings
from django.http import JsonResponse
# Create your views here.

def login_check(func):
    def inner(request,*args,**kwargs):
        user = request.session.get('username')
        if not user:
            return redirect('/user/login/')
        res = func(request,*args,**kwargs)
        return res
    return inner

@login_check
def family(request):
    familes = models.Family.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        familes = models.Family.objects.filter(name=name)

    return render(request,'family/depart.html',locals())
    # def post(self,request):
    #     name = request.POST['name']
    #     photo = request.POST['photo']
    #     models.Family.objects.update_or_create(name=name,photo=photo)
    #     return redirect('/family/')
@login_check
def familyAdd(request):
    obj = request.user
    if request.method == 'POST':
        name = request.POST['departName']
        photo = request.POST['upload']
        models.Family.objects.filter(name=obj).create(name=name,photo=photo)
        return redirect('/family/')
    return render(request, 'family/addDepart.html', locals())


def familyAddDepartLayer(request):
    ret = {"success": False, "context": {"msg":""}}
    if request.method == "POST":
        data = simplejson.loads(request.body.decode())
        name = data["name"]
        initial = data["initial"]
        num = models.Family.objects.create(name=name)
        if num:
            ret['success'] = True
            ret['context'] ['msg'] = '添加成功'
        else:
            ret['success'] = False
            ret['context']['msg'] = '失败了'
        return JsonResponse(ret)
    return render(request, 'family/addDepartLayer.html', locals())
import simplejson
def familyEditDepartLayer(request):
    ret = {"success": False, "context": {"msg":""}}
    if request.method == "POST":
        data = simplejson.loads(request.body.decode())
        id = data["id"]
        name = data["name"]
        num = models.Family.objects.update(id=id,name=name)
        if num >= 1:
            ret['success'] = True
            ret['context'] ['msg'] = '编辑成功'
        else:
            ret['success'] = False
            ret['context']['msg'] = '失败了'
        return JsonResponse(ret)

    return render(request, 'family/editDepartLayer.html', locals())


def familyAddDepart(request):
    ret = {"success":False, "context":""}
    #TODO： 解析json数据，写入库 如果成功，返回 {success:True,context:{msg:成功}
    #如果失败未知原因 返回{success:False,context:{msg:失败}
    #如果失败 已知原因  返回{success:False,context:{msg:原因}

    return JsonResponse(ret)


@login_check
def familyUpdate(request,id):
    obj = models.Family.objects.filter(id=id)
    if request.method == 'POST':
        name = request.POST['departName']
        f1 = request.FILES.get('upload')
        photo = 'familyMember/'+ f1.name
        photoName = settings.MEDIA_ROOT.replace('\\', '/') + "/familyMember/" + f1.name
        with open(photoName,'wb') as f:
            for content in f1.chunks():
                f.write(content)
        obj.update(name=name,photo=photo)
        return redirect('/family/')
    return render(request,'family/updateDepart.html',locals())
@login_check
def familyDelete(request,id):
    obj = models.Family.objects.filter(id=id)
    obj.delete()
    return redirect('/family/')
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
@login_check
def warning(request):
    return render(request,'warning/demo.html')


def train(request,id):
    obj = models.Family.objects.filter(id=id).first()
    img = obj.photo
    ret = {"img":img}
    return  JsonResponse(ret)
