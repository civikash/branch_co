from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('reports/', include('reports.urls')),
    path('admin-control/', include('admin_control.urls'))
]
