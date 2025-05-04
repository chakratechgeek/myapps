from django.urls import path
from .views import add_software_api, list_software_api
from .views import collect_software_api, get_python_script

urlpatterns = [
    path('api/add/', add_software_api),
    path('api/list/', list_software_api),
    path('api/get-script/', get_python_script),
    path('api/collect/', collect_software_api),

]
