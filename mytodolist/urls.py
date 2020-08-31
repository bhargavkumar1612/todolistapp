"""mytodolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from todoapp import views

urlpatterns = [
	path('', views.signinuser, name = 'signinuser'),
	path('home/', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signupuser, name = 'signupuser'),
    path('logoutuser/', views.logoutuser, name = 'logoutuser'),
    path('signinuser/', views.signinuser, name = 'signinuser'),
    path('currenttodos/', views.currenttodos, name = 'currenttodos'),
    path('create/', views.createtodo, name = 'createtodo'),
    path('todo/<int:todo_pk>', views.viewtodo, name = 'viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name = 'completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name = 'deletetodo'),
    path('todo/<int:todo_pk>/readdtodo', views.readdtodo, name = 'readdtodo'),
    path('todo/<int:todo_pk>/edittodo', views.edittodo, name = 'edittodo'),
]