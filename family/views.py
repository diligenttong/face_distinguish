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
    return render(request, 'family/addDepartLayer.html', locals())

def familyEditDepartLayer(request):
    return render(request, 'family/editDepartLayer.html', locals())



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
