from django.urls import path
from . import views


urlpatterns =[
    path('',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('app/',views.app,name="app"),
    path('result/',views.result,name="result")
]