from django.urls import path
from django.contrib.auth.decorators import login_required
from reports.views import reports, balanta, reports_add, reports_delete, economica, privind, cadrelor, investiti, strocuri

app_name = 'reports'

urlpatterns = [
    path('delete-marfa/<int:code>/', reports_delete.delete_marfa, name='delete_marfa'),
    path('delete-investi/<int:code>/', reports_delete.delete_investiti, name='delete_investiti'),
    path('economica/', login_required(economica.InfEconOpCreateView.as_view(), login_url='/login/'), name='economica-views'),
    path('strocuri/', login_required(strocuri.StrocuriListView.as_view(), login_url='/login/'), name='strocuri'),
    path('strocuri/<uuid:uid>/', login_required(strocuri.StrocuriDetail.as_view(), login_url='/login/'), name='strocuri-detail'),
    path('balanta/', login_required(balanta.BalantaListView.as_view(), login_url='/login/'), name='balanta'),
    path('balanta/<uuid:uid>/', login_required(balanta.BalantaDetail.as_view(), login_url='/login/'), name='balanta-detail'),
    path('privind/', login_required(privind.PrivindListView.as_view(), login_url='/login/'), name='privinds'),
    path('privind/<uuid:uid>/', login_required(privind.PrivindDetail.as_view(), login_url='/login/'), name='privind-detail'),
    path('investi/', login_required(investiti.InvestitiListView.as_view(), login_url='/login/'), name='investis'),
    path('investi/<uuid:uid>/', login_required(investiti.InvestitiDetail.as_view(), login_url='/login/'), name='investi-detail'),
    path('cadrelor/', login_required(cadrelor.CadrelorListView.as_view(), login_url='/login/'), name='cadrelor'),
    path('cadrelor/<uuid:uid>/', login_required(cadrelor.CadrelorDetailView.as_view(), login_url='/login/'), name='cadrelor-detail'),
    path('repots/<uuid:uid>/', login_required(reports_add.ReportsAdds.as_view(), login_url='/login/'), name='reports-vision'),
    path('details/<int:counter>/', login_required(reports.ReportDetails.as_view(), login_url='/login/'), name='report-details'),
    path('', login_required(reports.ReportsList.as_view(), login_url='/login/'), name='reports')
]
