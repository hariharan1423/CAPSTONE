from django.urls import path
from . import views


urlpatterns =[
    path('',views.app,name="app"),
    path('result/',views.result,name="result")
]