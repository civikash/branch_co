from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import Q
from itertools import chain
from reports.models import ManagerInfEconOp, ManagerMiscCadrelor, ManagerRaportStatisticTrimestrial, ManagerRaportStocuri, ManagerReportDescriereaAsociati



class ReportsList(View):
    template_name = 'admin_control/raports_all.html'

    def get(self, request, *args, **kwargs):
        reports_1 = ManagerInfEconOp.objects.all()
        reports_2 = ManagerMiscCadrelor.objects.all()
        reports_3 = ManagerRaportStatisticTrimestrial.objects.all()
        reports_4 = ManagerRaportStocuri.objects.all() #{% url 'reports:strocuri-detail' uid=report.uid %}
        reports_5 = ManagerReportDescriereaAsociati.objects.all() #{% url 'reports:privind-detail' uid=report.uid %}


        context = {'reports_1': reports_1, 'reports_2': reports_2, 'reports_3': reports_3, 'reports_4': reports_4, 'reports_5': reports_5,}
        return render(request, self.template_name, context)