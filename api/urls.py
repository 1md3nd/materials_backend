from django.urls import path, include
from .views import home, get_all_materials, search_materials_formula,compare_fields,boolen_filter,validate_field,search_text

urlpatterns = [
    path("", home, name="home"),
    path("get_all_materials/", get_all_materials, name='materials'),
    path("search_materials/", search_materials_formula, name='search-materials'),
    path("compare_fields/", compare_fields, name='compare-fields'),
    path("boolen/<str:field>:<str:value>", boolen_filter, name='boolen-fiter'),
    path("validate", validate_field, name='boolen-fiter'),
    path("validate/<str:field>", validate_field, name='boolen-fiter'),
    path("search_text/", search_text, name='search-text'),

]
