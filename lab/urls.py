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
    path('gene_detail/<str:gene_id>', views.gene_detail, name='gene-detail'),
    path('compound_detail/<str:compound_id>', views.compound_detail, name="compound-detail"),
    path('get_compound_by_name/<str:compound_name>', views.get_compound_by_name, name='get-compound-by-name'),
    path('get_genes_by_name/<str:gene_name>', views.get_genes_by_name, name='get-genes-by-name'),
    path('get_compound_by_category/<str:category>', views.get_compound_by_category, name='get-compound-by-category'),
    path('get_known_targets/<str:compound_id>', views.get_known_targets, name='get-known-targets'),
    path('get_associated_targets/<str:compound_id>', views.get_associated_targets, name='get-associated-targets'),
    path('get_associated_compounds/<str:gene_id>', views.get_associated_compounds, name='get-associated-compounds'),
    path(
        'get_supported_entries_by_drug_id/<str:drug_id>',
        views.get_supported_entries_by_drug_id,
        name='get-supported-entries-by-drug-id'
    ),
    path(
        'get_supported_entries_by_ids/<str:target_id>/<str:drug_id>',
        views.get_supported_entries_by_ids,
        name='get-supported-entries-by-ids'
    ),
    path('statistics', views.statistics, name='statistics'),
    path('help', views.help, name='help'),
    path('get_score_frequency/<str:id>', views.get_score_frequency, name='score-frequency')
]
