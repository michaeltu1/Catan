from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('test/', views.test_json, name='test'),
    path('testReact/', views.react_test, name='rTest')
]
