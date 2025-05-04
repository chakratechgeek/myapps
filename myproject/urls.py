from django.contrib import admin
from django.urls import path, include
from inventory.views import get_powershell_script  # 👈 Import your view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('person/', include('person.urls')),
    path('software/', include('inventory.urls')),
    path('software/api/get-script/', get_powershell_script),
     path('software/', include('inventory.urls')),  # ✅ ensures /software/api/collect/ works
]
