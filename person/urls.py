from django.urls import path
from .views import add_person_api, list_person_api

urlpatterns = [
    path('api/add/', add_person_api, name='add_person_api'),
    path('api/list/', list_person_api, name='list_person_api'),
]
