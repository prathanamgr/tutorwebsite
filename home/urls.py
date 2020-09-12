from django.urls import path

from home import views

urlpatterns=[
    path('',views.show),
    path('contact/',views.contact),
    path('about/',views.about),
    path('tutors/',views.tutors)
]