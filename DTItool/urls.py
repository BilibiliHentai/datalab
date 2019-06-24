from django.urls import path
from DTItool import views

app_name = 'DTItool'


urlpatterns = [
    path('', views.index, name='index'),
    path('startup', views.startup, name='startup'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('search/drug/<str:drug_name>', views.search_for_drug, name='search_drug'),
    path('search/protein/<str:protein_name>', views.search_for_protein, name='search_protein'),
    path('condition/drug/<str:drug_name>/<str:dtinet_upper_limit>/<str:dtinet_lower_limit>/<str:neodti_upper_limit>/<str:neodti_lower_limit>', views.condition_for_drug, name='condition_drug'),
    path("condition/protein/<str:protein_name>/<str:dtinet_upper_limit>/<str:dtinet_lower_limit>/<str:neodti_upper_limit>/<str:neodti_lower_limit>", views.condition_for_protein, name="condition_protein"),
    path('ranking/drug/<str:drug_name>/<int:dtinet_upper_ranking>/<int:dtinet_lower_ranking>/<int:neodti_upper_ranking>/<int:neodti_lower_ranking>', views.ranking_for_drug, name='ranking_drug'),
    path('ranking/protein/<str:drug_name>/<int:dtinet_upper_ranking>/<int:dtinet_lower_ranking>/<int:neodti_upper_ranking>/<int:neodti_lower_ranking>', views.ranking_for_protein, name="ranking_protein"),
    path('search/protein/<str:protein_name>', views.search_for_protein, name="search_protein"),
    path('excel/drug/<str:drug_name>', views.drug_excel, name='drug_excel'),
    path('excel/protein/<str:protein_name>', views.excel_for_protein, name='protein_excel'),
    path('excel/drug/<str:drug_name>/dtinet/', views.drug_excel_dtinet, name='drug_excel_dtinet'),
    path('excel/drug/<str:drug_name>/neodti/', views.drug_excel_neodti, name='drug_excel_neodti'),
    path('excel/condition/drug/<str:drug_name>/<str:dtinet_upper_limit>/<str:dtinet_lower_limit>/<str:neodti_upper_limit>/<str:neodti_lower_limit>', views.excel_condition),
    path('excel/ranking/drug/<str:drug_name>/<int:dtinet_upper_ranking>/<int:dtinet_lower_ranking>/<int:neodti_upper_ranking>/<int:neodti_lower_ranking>', views.excel_ranking),
    path('excel/condition/protein/<str:protein_name>/<str:dtinet_upper_limit>/<str:dtinet_lower_limit>/<str:neodti_upper_limit>/<str:neodti_lower_limit>', views.excel_condition_protein),
    path('excel/ranking/protein/<str:protein_name>/<int:dtinet_upper_ranking>/<int:dtinet_lower_ranking>/<int:neodti_upper_ranking>/<int:neodti_lower_ranking>', views.excel_ranking_protein),
]