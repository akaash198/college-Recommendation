from django.urls import path
from .import views
urlpatterns=[
    path('',views.main,name='main'),
    path('cr',views.home,name='home'),
    path('br',views.home1,name='home1'),
    path('lr',views.home2,name='home2'),
    path('college/',views.college,name='college'),
    path('branch/',views.branch,name='branch'),
    path('result/',views.result,name='result'),
    path('empty/',views.empty,name='empty'),
    path('bresult/',views.bresult,name='bresult'),
    path('lresult/',views.lresult,name='lresult')
    
     
]
