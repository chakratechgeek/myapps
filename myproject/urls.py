from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('person/', include('person.urls')),    
    path('software/', include('inventory.urls')),
]
