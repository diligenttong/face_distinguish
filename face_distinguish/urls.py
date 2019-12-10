"""face_distinguish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from face_distinguish import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path,re_path
from family import views as view
from User import views
from face_distinguish import views as view1
urlpatterns = [
    path('',views.login,name='login'),
    path('/',views.login,name='login'),
    path('admin/', admin.site.urls),
    path('home/', view1.home, name='home'),
    path('user/login/',views.login,name='login'),
    path('user_logout/',views.user_logout,name='user_logout'),

    path('family/',view.family,name='family'),
    path('family/add/', view.familyAdd, name='familyAdd'),
    path('family/add_depart_layer', view.familyAddDepartLayer, name='familyAddDepartLayer'),
    path('family/edit_depart_layer', view.familyEditDepartLayer, name='familyEditDepartLayer'),
    path('family/edit/<int:id>/',view.familyUpdate,name='familyUpdate'),
    path('family/del/<int:id>/', view.familyDelete, name='familyDelete'),


    path('warning/', view.warning, name='warning'),
    path('handle/', view1.handleIndex, name='HandleIndex'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('train/<int:id>',view.train,name='train'),



]
