from django.urls import path
from . import views

app_name = 'lab'


urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:keyword>/<int:page>', views.index, name='index'),
    path('', views.index, name='index'),
    path('statistics', views.statistics, name='statistics'),
]
