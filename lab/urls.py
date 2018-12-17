from django.urls import path
from . import views

app_name = 'lab'


urlpatterns = [
    path('', views.index, name='index'),
    path('gene', views.gene, name='gene'),
    path('gene/<str:gene_name>', views.gene_detail, name='gene-detail'),
    path('compound', views.compound, name='compound'),
    path('compound/<str:compound_name>', views.compound_detail, name="compound-detail"),
    path('statistics', views.statistics, name='statistics'),
    path('help', views.help, name='help'),
    path('get_score_frequency', views.get_score_frequency, name='score-frequency')
]
