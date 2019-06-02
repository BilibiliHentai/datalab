from django.urls import path
from . import views

app_name = 'DTItool'


urlpatterns = [
    path('', views.index, name='index'),
    path('startup', views.startup, name='startup'),
    path('search/drug/<str:drug_name>', views.search_for_drug, name='search_drug'),
    path('search/protein/<str:protein_name>', views.search_for_protein, name="search_protein")
]