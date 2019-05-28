from django.urls import path
from . import views

app_name = 'DTItool'


urlpatterns = [
    path('', views.index, name='index'),
    path('startup', views.startup, name='startup'),
    path('search/<str:drug_name>', views.search_for_drug, name='search')
]