from django.urls import path
from . import views

app_name = 'lab'


urlpatterns = [
    path('', views.index, name='index'),
    path('gene', views.gene, name='gene'),
    path('compound', views.compound, name='compound'),
    path('statistics', views.statistics, name='statistics'),
    path('help', views.help, name='help'),
]
