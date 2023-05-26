from django.urls import path
from django.contrib.auth.decorators import login_required
from reports.views import reports, reports_add

app_name = 'reports'

urlpatterns = [
    path('api/rows/', reports_add.RowsAPI.as_view(), name='rows_api'),
    path('registry/', login_required(reports_add.ReportsAdds.as_view(), login_url='/login/'), name='reports-add'),
    path('details/<int:counter>/', login_required(reports.ReportDetails.as_view(), login_url='/login/'), name='report-details'),
    path('', login_required(reports.ReportsList.as_view(), login_url='/login/'), name='reports')
]
