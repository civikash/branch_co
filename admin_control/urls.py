from django.urls import path
from django.contrib.auth.decorators import login_required
from admin_control.views import control

app_name = 'admin_control'

urlpatterns = [
    path('reports/', login_required(control.ReportsList.as_view(), login_url='/login/'), name='reports-admin')
]
