from django.shortcuts import render
def home(request):
    return render(request,'home.html')

def handleIndex(request):
    return render(request,'user/index.html')