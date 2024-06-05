"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from app01 import views as app01_view

urlpatterns = [
    path("", app01_view.sql_list),
    path("depart/add/", app01_view.depart_add),
    path("depart/del/", app01_view.depart_del),
    path("depart/list/", app01_view.depart_list),
    path("depart/edit/", app01_view.depart_edit),
    path("depart/<int:req_id>/edit/", app01_view.depart_edit2),
    
    path("user/list/", app01_view.user_list),
    path("user/add/", app01_view.user_add),
    path("user/<int:uid>/edit/", app01_view.user_edit),
    path("user/<int:pid>/delete/", app01_view.user_delete),


    path("pretty/list/", app01_view.pretty_list),
    path("pretty/add/", app01_view.pretty_add),
    path("pretty/<int:pid>/edit/", app01_view.pretty_edit),
    path("pretty/<int:pid>/delete/", app01_view.pretty_delete),


    path("admin/", admin.site.urls),
]
