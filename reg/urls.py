from django.urls import path

from reg import views

urlpatterns=[
    path('',views.login),
    path('register/',views.register),
    path('teacher/',views.teacherReg),
    path('logout/',views.logout)
]