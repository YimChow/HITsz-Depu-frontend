"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
import django
from my_web import views
from assess import views as v2
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import staticfiles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('mainrules/', views.mainrules, name='mainrules'),
    path('teachrules/', views.teachrules, name='teachrules'),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('introduction/', views.introduction, name='introduction'),
    path('user/login', views.login, name='login'),
    path('assess/', v2.assess, name='assess'),

]
# 设置静态文件路径
urlpatterns += staticfiles_urlpatterns()

# Examples:
# Function views
# 1. Add an import:  from my_app import views
# 2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
# 1. Add an import:  from other_app.views import Home
# 2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
# 1. Import the include() function: from django.urls import include, path
# 2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
