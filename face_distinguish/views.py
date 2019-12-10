from django.shortcuts import render
from User.models import Family
def home(request):
    return render(request,'home.html')

def handleIndex(request):
    all_queryset = Family.objects.all()
    print(request.body)
    return render(request,'user/index.html',locals())

# def familyAddDepartLayer(request):
#     return render(request,'family/addDepartLayer.html')