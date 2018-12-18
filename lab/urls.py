from django.urls import path
from . import views

app_name = 'lab'


urlpatterns = [
    path('', views.index, name='index'),
    path('gene', views.gene, name='gene'),
    path('gene/<str:gene_name>', views.gene_detail, name='gene-detail'),
    # path('search_compound/<str:compound_name>', views.compound, name='compound'),
    path('compound', views.compound, name='compound'),
    path('compound/<str:category>', views.compound, name='compound'),
    path('get_compound_by_name/<str:compound_name>', views.get_compound_by_name, name='get-compound-by-name'),
    path('get_compound_by_category/<str:category>', views.get_compound_by_category, name='get-compound-by-category'),
    path('compound_detail/<str:compound_name>', views.compound_detail, name="compound-detail"),
    path('statistics', views.statistics, name='statistics'),
    path('help', views.help, name='help'),
    path('get_score_frequency', views.get_score_frequency, name='score-frequency')
]
